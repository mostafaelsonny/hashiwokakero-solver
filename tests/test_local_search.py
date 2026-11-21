"""Unit tests for local search operators on the canonical P1 fixture."""
import copy

import pytest

from core.graph_context import GraphContext
from algorithms.memetic import (
    InvalidChromosomeError,
    find_invalid_values,
    generate_neighbors,
    pairwise_transfer_neighbors,
    single_gene_neighbors,
    _actual_degrees,
)

PUZZLE = {
    "rows": 3, "cols": 3,
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


def make_ctx(use_ids=False):
    inc = INCIDENT if not use_ids else {
        k: [BRIDGES[i]["id"] for i in v] for k, v in INCIDENT.items()}
    return GraphContext(inc, {0: [], 1: [], 2: [], 3: []})


@pytest.fixture
def ctx():
    return make_ctx()


def deg(chrom, island):
    return _actual_degrees(chrom, BRIDGES).get(island, 0)


def legal(nb):
    return (isinstance(nb, list) and len(nb) == 4
            and all(type(g) is int and g in (0, 1, 2) for g in nb))


# ---- Operator 1 ----------------------------------------------------------
def test_single_gene_counts_and_domain():
    nbs = single_gene_neighbors(SOLUTION)
    assert len(nbs) == 8
    assert [1, 0, 1, 1] in nbs and [1, 2, 1, 1] in nbs
    for nb in nbs:
        assert legal(nb)
        assert sum(a != b for a, b in zip(nb, SOLUTION)) == 1


# ---- Operator 2 ----------------------------------------------------------
def test_pairwise_focal_degree_preserved_exact(ctx):
    chrom = [2, 0, 1, 1]            # A=2 ok, B=3 (excess), C=1 (deficit), D=2 ok
    nbs = pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert sorted(nbs) == sorted([[1, 0, 2, 1], [2, 1, 1, 0]])
    # first: focal B (E1 -> E3): B's degree unchanged, A and D change
    assert deg([1, 0, 2, 1], "B") == deg(chrom, "B") == 3
    assert deg([1, 0, 2, 1], "A") == deg(chrom, "A") - 1
    assert deg([1, 0, 2, 1], "D") == deg(chrom, "D") + 1
    # second: focal C (E4 -> E2): C's degree unchanged, A and D change
    assert deg([2, 1, 1, 0], "C") == deg(chrom, "C") == 1
    assert deg([2, 1, 1, 0], "A") == deg(chrom, "A") + 1
    assert deg([2, 1, 1, 0], "D") == deg(chrom, "D") - 1


def test_pairwise_2_0_to_1_1(ctx):
    chrom = [2, 0, 0, 0]            # A is balanced -> skipped by default
    assert [1, 1, 0, 0] not in pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    nbs = pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx, only_unbalanced=False)
    assert [1, 1, 0, 0] in nbs
    assert deg([1, 1, 0, 0], "A") == deg(chrom, "A") == 2


def test_pairwise_respects_gene_limits(ctx):
    assert pairwise_transfer_neighbors([2, 2, 2, 2], PUZZLE, BRIDGES, ctx,
                                       only_unbalanced=False) == []
    for chrom in ([0, 0, 0, 0], [2, 0, 2, 0], [0, 2, 0, 2]):
        for nb in pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, ctx,
                                              only_unbalanced=False):
            assert legal(nb)


def test_balanced_solution_has_no_transfers(ctx):
    assert pairwise_transfer_neighbors(SOLUTION, PUZZLE, BRIDGES, ctx) == []


def test_graph_context_with_bridge_ids_same_result():
    chrom = [2, 0, 1, 1]
    assert (pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, make_ctx(False))
            == pairwise_transfer_neighbors(chrom, PUZZLE, BRIDGES, make_ctx(True)))


def test_unknown_bridge_id_in_context_raises_clear_error():
    bad = GraphContext({"A": ["E99"], "B": [], "C": [], "D": []}, {})
    with pytest.raises(ValueError, match="E99"):
        pairwise_transfer_neighbors([0, 0, 0, 0], PUZZLE, BRIDGES, bad)


# ---- Generator -----------------------------------------------------------
@pytest.mark.parametrize("chrom", [[0, 0, 0, 0], [1, 1, 1, 1], [2, 0, 1, 1],
                                   [2, 2, 2, 2], [0, 2, 0, 2]])
def test_generate_neighbors_strictly_valid(chrom, ctx):
    nbs = generate_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert nbs
    assert len({tuple(n) for n in nbs}) == len(nbs)
    assert tuple(chrom) not in {tuple(n) for n in nbs}
    assert all(legal(nb) for nb in nbs)


def test_generate_contains_both_operators(ctx):
    nbs = generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx)
    assert [2, 0, 1, 2] in nbs and [1, 0, 2, 1] in nbs and [2, 1, 1, 0] in nbs


def test_original_never_mutated(ctx):
    chrom = [2, 0, 1, 1]
    snap = copy.deepcopy((chrom, PUZZLE, BRIDGES))
    nbs = generate_neighbors(chrom, PUZZLE, BRIDGES, ctx)
    assert (chrom, PUZZLE, BRIDGES) == snap
    assert all(nb is not chrom for nb in nbs)
    nbs[0][0] = 99
    assert chrom == [2, 0, 1, 1]


def test_deterministic(ctx):
    assert (generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx)
            == generate_neighbors([2, 0, 1, 1], PUZZLE, BRIDGES, ctx))


# ---- Invalid input (Section 8.5 shape) ----------------------------------
@pytest.mark.parametrize("bad", [[1, 3, 1, 1], [1, -1, 1, 1], [1, "1", 1, 1],
                                 [1, 1.0, 1, 1], [1, True, 1, 1]])
def test_bad_gene_reported_not_coerced(bad, ctx):
    with pytest.raises(InvalidChromosomeError) as exc:
        generate_neighbors(bad, PUZZLE, BRIDGES, ctx)
    assert isinstance(exc.value, ValueError)
    assert exc.value.invalid_values == [{
        "path": "chromosome[1]", "value": bad[1],
        "reason": "chromosome_gene_must_be_integer_0_1_or_2"}]


@pytest.mark.parametrize("bad", [[1, 1, 1], [1, 1, 1, 1, 1]])
def test_length_mismatch_reported(bad, ctx):
    issues = find_invalid_values(bad, BRIDGES)
    assert {"path": "chromosome", "value": len(bad),
            "reason": "chromosome_length_mismatch"} in issues
    with pytest.raises(InvalidChromosomeError):
        generate_neighbors(bad, PUZZLE, BRIDGES, ctx)
        