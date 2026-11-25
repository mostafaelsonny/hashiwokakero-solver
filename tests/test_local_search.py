"""Unit tests for Memetic Local Search Operators (Sprint 2 - S2-09).

Tests:
1. Operator 1: Single Gene Perturbation (bounds checking, domain {0, 1, 2}, non-mutation).
2. Operator 2: Pairwise Bridge Transfer (focal degree invariant, gene limits, opposite adjustments).
3. Neighborhood Generator: strictly legal candidate chromosomes, determinism, deduplication.
4. Input validation adhering to docs/DATA_MODEL.md Sections 7.2, 8.5, and 11.3.
5. Integration with M4 fitness evaluation and problem-aware Hill Climbing on P1 fixture.
"""
from __future__ import annotations

import copy
import pytest

from core.graph_context import GraphContext, build_graph_context
from algorithms.ma.local_search import (
    InvalidChromosomeError,
    best_improving_neighbor,
    conflict_pairs_from_graph_context,
    evaluate_chromosome,
    find_invalid_values,
    generate_neighbors,
    hill_climb,
    pairwise_transfer_neighbors,
    single_gene_neighbors,
    validate_local_search_input,
    _actual_degrees,
)
import algorithms.memetic as memetic_module

# ---- Canonical P1 Fixture (docs/DATA_MODEL.md Section 9) -----------------------
PUZZLE = {
    "rows": 3,
    "cols": 3,
    "islands": [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
        {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
        {"id": "C", "row": 2, "col": 0, "required_bridges": 2},
        {"id": "D", "row": 2, "col": 2, "required_bridges": 2},
    ],
}
BRIDGES = [
    {"id": "E1", "from": "A", "to": "B", "orientation": "horizontal"},
    {"id": "E2", "from": "A", "to": "C", "orientation": "vertical"},
    {"id": "E3", "from": "B", "to": "D", "orientation": "vertical"},
    {"id": "E4", "from": "C", "to": "D", "orientation": "horizontal"},
]
SOLUTION = [1, 1, 1, 1]
INCIDENT = {"A": [0, 1], "B": [0, 2], "C": [1, 3], "D": [2, 3]}


def make_ctx(use_ids: bool = False) -> GraphContext:
    """Build a GraphContext fixture with either integer indices or bridge IDs."""
    inc = (
        INCIDENT
        if not use_ids
        else {k: [BRIDGES[i]["id"] for i in v] for k, v in INCIDENT.items()}
    )
    islands_map = {isl["id"]: isl for isl in PUZZLE["islands"]}
    return GraphContext(
        islands_by_id=islands_map,
        candidate_bridges=BRIDGES,
        incident_edges_by_island=inc,
        crossing_edges_by_index={0: [], 1: [], 2: [], 3: []},
    )


@pytest.fixture
def ctx() -> GraphContext:
    return make_ctx()


@pytest.fixture
def real_ctx() -> GraphContext:
    """GraphContext built using M2's official build_graph_context generator."""
    return build_graph_context(PUZZLE, BRIDGES)


def deg(chrom: list[int], island: str) -> int:
    return _actual_degrees(chrom, BRIDGES).get(island, 0)


def legal(nb: list[int]) -> bool:
    return (
        isinstance(nb, list)
        and len(nb) == 4
        and all(type(g) is int and g in (0, 1, 2) for g in nb)
    )


# ==============================================================================
# Operator 1: Single Gene Perturbation
# ==============================================================================
def test_single_gene_counts_and_domain():
    nbs = single_gene_neighbors(SOLUTION)
    # 4 genes * 2 alternate values in {0, 1, 2} = 8 neighbors
    assert len(nbs) == 8
    assert [1, 0, 1, 1] in nbs and [1, 2, 1, 1] in nbs
    for nb in nbs:
        assert legal(nb)
        assert sum(a != b for a, b in zip(nb, SOLUTION)) == 1


def test_single_gene_specific_index():
    # Perturb only gene at index 1 (originally 1) -> generates 0 and 2 at index 1
    nbs = single_gene_neighbors([1, 1, 1, 1], gene_index=1)
    assert len(nbs) == 2
    assert [1, 0, 1, 1] in nbs
    assert [1, 2, 1, 1] in nbs
    assert all(nb[0] == 1 and nb[2] == 1 and nb[3] == 1 for nb in nbs)


def test_single_gene_out_of_bounds_index():
    with pytest.raises(ValueError, match="out of range"):
        single_gene_neighbors([1, 1, 1, 1], gene_index=10)


# ==============================================================================
# Operator 2: Pairwise Bridge Transfer
# ==============================================================================
def test_pairwise_focal_degree_preserved_exact(ctx):
    chrom = [2, 0, 1, 1]  # A=2 (ok), B=3 (excess), C=1 (deficit), D=2 (ok)
    nbs = pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert sorted(nbs) == sorted([[1, 0, 2, 1], [2, 1, 1, 0]])

    # Move 1: focal B (E1 -> E3): B's degree is UNCHANGED (3 -> 3)
    assert deg([1, 0, 2, 1], "B") == deg(chrom, "B") == 3
    # Opposite endpoints adjust
    assert deg([1, 0, 2, 1], "A") == deg(chrom, "A") - 1
    assert deg([1, 0, 2, 1], "D") == deg(chrom, "D") + 1

    # Move 2: focal C (E4 -> E2): C's degree is UNCHANGED (1 -> 1)
    assert deg([2, 1, 1, 0], "C") == deg(chrom, "C") == 1
    # Opposite endpoints adjust
    assert deg([2, 1, 1, 0], "A") == deg(chrom, "A") + 1
    assert deg([2, 1, 1, 0], "D") == deg(chrom, "D") - 1


def test_pairwise_with_real_graph_context(real_ctx):
    chrom = [2, 0, 1, 1]
    nbs = pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, real_ctx)
    assert sorted(nbs) == sorted([[1, 0, 2, 1], [2, 1, 1, 0]])


def test_pairwise_2_0_to_1_1(ctx):
    chrom = [2, 0, 0, 0]  # Island A has degree 2 (balanced) -> skipped by default
    assert [1, 1, 0, 0] not in pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx)

    # When only_unbalanced=False, focal island A can transfer E1 -> E2 (2,0 -> 1,1)
    nbs = pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx, only_unbalanced=False)
    assert [1, 1, 0, 0] in nbs
    assert deg([1, 1, 0, 0], "A") == deg(chrom, "A") == 2


def test_pairwise_focal_island_explicit(ctx):
    chrom = [2, 0, 1, 1]
    # Restrict to focal island B only
    nbs_b = pairwise_transfer_neighbors(
        chrom, PUZZLE, BRIDGES, ctx, only_unbalanced=False, focal_island_id="B"
    )
    assert nbs_b == [[1, 0, 2, 1]]


def test_pairwise_respects_gene_limits(ctx):
    # All 2s cannot increment
    assert pairwise_transfer_neighbors([2, 2, 2, 2], PUZZLE, BRIDGES, ctx, only_unbalanced=False) == []
    # All 0s cannot decrement
    assert pairwise_transfer_neighbors([0, 0, 0, 0], PUZZLE, BRIDGES, ctx, only_unbalanced=False) == []

    for chrom in ([0, 0, 0, 0], [2, 0, 2, 0], [0, 2, 0, 2]):
        for nb in pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx, only_unbalanced=False):
            assert legal(nb)


def test_balanced_solution_has_no_transfers(ctx):
    # Balanced solution produces 0 transfers when only_unbalanced=True
    assert pairwise_transfer_neighbors(SOLUTION, PUZZLE, BRIDGES, ctx) == []


def test_graph_context_with_bridge_ids_same_result():
    chrom = [2, 0, 1, 1]
    assert (
        pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, make_ctx(False))
        == pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, make_ctx(True))
    )


def test_unknown_bridge_id_in_context_raises_clear_error():
    bad = GraphContext(
        islands_by_id={},
        candidate_bridges=BRIDGES,
        incident_edges_by_island={"A": ["E99"], "B": [], "C": [], "D": []},
    )
    with pytest.raises(ValueError, match="E99"):
        pairwise_transfer_neighbors([0, 0, 0, 0], PUZZLE, BRIDGES, bad, only_unbalanced=False)


# ==============================================================================
# Neighborhood Generator
# ==============================================================================
@pytest.mark.parametrize(
    "chrom",
    [[0, 0, 0, 0], [1, 1, 1, 1], [2, 0, 1, 1], [2, 2, 2, 2], [0, 2, 0, 2]],
)
def test_generate_neighbors_strictly_valid(chrom, ctx):
    nbs = generate_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert nbs
    assert len({tuple(n) for n in nbs}) == len(nbs)
    assert tuple(chrom) not in {tuple(n) for n in nbs}
    assert all(legal(nb) for nb in nbs)


def test_generate_contains_both_operators(ctx):
    nbs = generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx)
    # From Operator 1 (Single Gene Perturbation):
    assert [2, 0, 1, 2] in nbs
    # From Operator 2 (Pairwise Bridge Transfer):
    assert [1, 0, 2, 1] in nbs
    assert [2, 1, 1, 0] in nbs


def test_original_never_mutated(ctx):
    chrom = [2, 0, 1, 1]
    snap = copy.deepcopy((chrom, PUZZLE, BRIDGES))
    nbs = generate_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert (chrom, PUZZLE, BRIDGES) == snap
    assert all(nb is not chrom for nb in nbs)
    nbs[0][0] = 99
    assert chrom == [2, 0, 1, 1]


def test_deterministic(ctx):
    assert (
        generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx)
        == generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx)
    )


def test_generate_neighbors_with_none_graph_context():
    # Automatically builds GraphContext if None is passed
    nbs = generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, None)
    assert [1, 0, 2, 1] in nbs
    assert all(legal(nb) for nb in nbs)


# ==============================================================================
# Invalid input reporting (docs/DATA_MODEL.md Sections 7.2, 8.5, 11.3)
# ==============================================================================
@pytest.mark.parametrize(
    "bad",
    [[1, 3, 1, 1], [1, -1, 1, 1], [1, "1", 1, 1], [1, 1.0, 1, 1], [1, True, 1, 1]],
)
def test_bad_gene_reported_not_coerced(bad, ctx):
    with pytest.raises(InvalidChromosomeError) as exc:
        generate_neighbors(bad, PUZZLE, BRIDGES, ctx)
    assert isinstance(exc.value, ValueError)
    assert exc.value.invalid_values == [
        {
            "path": "chromosome[1]",
            "value": bad[1],
            "reason": "chromosome_gene_must_be_integer_0_1_or_2",
        }
    ]


@pytest.mark.parametrize("bad", [[1, 1, 1], [1, 1, 1, 1, 1]])
def test_length_mismatch_reported(bad, ctx):
    issues = find_invalid_values(bad, BRIDGES)
    assert {
        "path": "chromosome",
        "value": len(bad),
        "reason": "chromosome_length_mismatch",
    } in issues
    with pytest.raises(InvalidChromosomeError):
        generate_neighbors(bad, PUZZLE, BRIDGES, ctx)


# ==============================================================================
# Fitness Integration & Hill Climbing
# ==============================================================================
def test_fitness_evaluation_and_conflicts_from_context(real_ctx):
    conflicts = conflict_pairs_from_graph_context(real_ctx)
    assert conflicts == []  # P1 has no crossing candidate pairs

    # Solution [1, 1, 1, 1] has zero degree error, zero crossings, zero connectivity penalty
    fitness_optimal = evaluate_chromosome(SOLUTION, PUZZLE, BRIDGES, graph_context=real_ctx)
    assert fitness_optimal == (0, 0, 0)

    # Suboptimal chromosome [2, 0, 1, 1]
    fitness_suboptimal = evaluate_chromosome([2, 0, 1, 1], PUZZLE, BRIDGES, graph_context=real_ctx)
    assert fitness_suboptimal > (0, 0, 0)


def test_best_improving_neighbor_strictly_improves(real_ctx):
    # Chromosome [1, 0, 1, 1] from FEBRONIA.md with penalty (2, 0, 0)
    chrom = [1, 0, 1, 1]
    initial_fitness = evaluate_chromosome(chrom, PUZZLE, BRIDGES, graph_context=real_ctx)
    assert initial_fitness == (2, 0, 0)

    result = best_improving_neighbor(chrom, PUZZLE, BRIDGES, graph_context=real_ctx)
    assert result is not None
    best_nb, best_fit = result
    assert best_fit < initial_fitness
    assert best_fit == (0, 0, 0)
    assert best_nb == SOLUTION


def test_hill_climb_reaches_solution_on_p1(real_ctx):
    # Starting from suboptimal chromosome [1, 0, 1, 1] (penalty 2 -> penalty 0)
    improved, stats = hill_climb(
        [1, 0, 1, 1], PUZZLE, BRIDGES, graph_context=real_ctx, max_steps=10
    )
    assert stats["improved"] is True
    assert stats["improvements"] > 0
    assert stats["final_fitness"] < stats["initial_fitness"]
    assert stats["final_fitness"] == [0, 0, 0]
    assert improved == SOLUTION

    # Also works on [2, 0, 1, 1] when only_unbalanced=False
    improved_unbal, stats_unbal = hill_climb(
        [2, 0, 1, 1], PUZZLE, BRIDGES, graph_context=real_ctx, max_steps=10, only_unbalanced=False
    )
    assert stats_unbal["improved"] is True
    assert improved_unbal == SOLUTION


def test_hill_climb_does_not_accept_worse_or_equal_when_optimal(real_ctx):
    # Starting from optimal solution [1, 1, 1, 1]
    improved, stats = hill_climb(
        SOLUTION, PUZZLE, BRIDGES, graph_context=real_ctx, max_steps=10
    )
    assert stats["improved"] is False
    assert stats["improvements"] == 0
    assert improved == SOLUTION
    assert stats["final_fitness"] == [0, 0, 0]


# ==============================================================================
# Backward Compatibility of algorithms.memetic module
# ==============================================================================
def test_memetic_module_exports_and_backward_compatibility():
    assert hasattr(memetic_module, "generate_neighbors")
    assert hasattr(memetic_module, "single_gene_neighbors")
    assert hasattr(memetic_module, "pairwise_transfer_neighbors")
    assert hasattr(memetic_module, "hill_climb")
    assert hasattr(memetic_module, "solve_memetic")
