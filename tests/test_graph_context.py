"""Unit tests for Core Graph Engine Context (S2 - M2)."""
from __future__ import annotations

import copy
import itertools
from typing import List

import pytest

from core.candidate_generator import generate_candidate_edges
from core.graph_context import build_graph_context
from core.models import CandidateBridge, Island, Puzzle


def _p1_fixture() -> tuple[Puzzle, List[CandidateBridge]]:
    """Canonical P1 puzzle from DATA_MODEL.md (3x3, A, B, C, D, no crossings)."""
    puzzle: Puzzle = {
        "rows": 3,
        "cols": 3,
        "islands": [
            {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
            {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
            {"id": "C", "row": 2, "col": 0, "required_bridges": 2},
            {"id": "D", "row": 2, "col": 2, "required_bridges": 2},
        ],
    }
    bridges = generate_candidate_edges(puzzle["islands"])
    return puzzle, bridges


def _p2_crossing_fixture() -> tuple[Puzzle, List[CandidateBridge]]:
    """Grid fixture containing a strict geometric crossing between H and V bridges.

    Layout (4x4):
      row 0: .  T  .  .      T at (0, 1)
      row 1: L  .  .  R      L at (1, 0), R at (1, 3) -> H bridge L-R at row 1, cols (0, 3)
      row 2: .  B  .  .      B at (2, 1) -> V bridge T-B at col 1, rows (0, 2)
      Intersection at (row=1, col=1): 0 < 1 < 3 and 0 < 1 < 2 -> strict crossing!
    """
    puzzle: Puzzle = {
        "rows": 4,
        "cols": 4,
        "islands": [
            {"id": "T", "row": 0, "col": 1, "required_bridges": 1},
            {"id": "L", "row": 1, "col": 0, "required_bridges": 1},
            {"id": "R", "row": 1, "col": 3, "required_bridges": 1},
            {"id": "B", "row": 2, "col": 1, "required_bridges": 1},
        ],
    }
    bridges = generate_candidate_edges(puzzle["islands"])
    return puzzle, bridges


def _irregular_grid_fixture() -> tuple[Puzzle, List[CandidateBridge]]:
    """Irregular grid with blocking island in middle and an isolated island.

    Layout (4x5):
      row 0: I1(0,0)  .  I2(0,2)  .  I3(0,4)
      row 1: .        .  .        .  .
      row 2: I4(2,0)  .  .        .  .
      row 3: .        .  .        .  ISO(3,4)  (isolated: no H/V neighbors)

    Sorted islands: I1(0,0), I2(0,2), I3(0,4), I4(2,0), ISO(3,4)
    Expected candidate bridges:
      - From I1(0,0): right -> I2(0,2) [H], down -> I4(2,0) [V]
      - From I2(0,2): right -> I3(0,4) [H]
      - From I3(0,4): down -> ISO(3,4) [V]
      - From I4(2,0): none
      - From ISO(3,4): none
    """
    puzzle: Puzzle = {
        "rows": 4,
        "cols": 5,
        "islands": [
            {"id": "ISO", "row": 3, "col": 4, "required_bridges": 1},
            {"id": "I3", "row": 0, "col": 4, "required_bridges": 2},
            {"id": "I1", "row": 0, "col": 0, "required_bridges": 3},
            {"id": "I4", "row": 2, "col": 0, "required_bridges": 1},
            {"id": "I2", "row": 0, "col": 2, "required_bridges": 2},
        ],
    }
    bridges = generate_candidate_edges(puzzle["islands"])
    return puzzle, bridges


def test_p1_incident_edges_and_no_crossings() -> None:
    """Verify P1 incident edge indices, deterministic order, and empty crossings."""
    puzzle, bridges = _p1_fixture()
    expected_ids = ["E1", "E2", "E3", "E4"]
    assert [b["id"] for b in bridges] == expected_ids

    ctx = build_graph_context(puzzle, bridges)

    assert [b["id"] for b in ctx.candidate_bridges] == expected_ids
    assert ctx.incident_edges_by_island == {
        "A": [0, 1],
        "B": [0, 2],
        "C": [1, 3],
        "D": [2, 3],
    }
    assert ctx.crossing_edges_by_index == {0: [], 1: [], 2: [], 3: []}
    assert ctx.get_incident_edges("A") == [0, 1]
    assert ctx.get_crossing_edges(0) == []
    assert ctx.would_edges_cross(0, 1) is False
    assert ctx.max_possible_degree("A") == 4


def test_deterministic_ordering_across_island_permutations() -> None:
    """Any input permutation of islands must yield identical bridges and context."""
    base_puzzle, base_bridges = _p1_fixture()
    base_ctx = build_graph_context(base_puzzle, base_bridges)

    for perm in itertools.permutations(base_puzzle["islands"]):
        permuted_puzzle: Puzzle = {
            "rows": base_puzzle["rows"],
            "cols": base_puzzle["cols"],
            "islands": [copy.deepcopy(isl) for isl in perm],
        }
        perm_bridges = generate_candidate_edges(permuted_puzzle["islands"])
        perm_ctx = build_graph_context(permuted_puzzle, perm_bridges)

        assert perm_bridges == base_bridges
        assert perm_ctx.incident_edges_by_island == base_ctx.incident_edges_by_island
        assert perm_ctx.crossing_edges_by_index == base_ctx.crossing_edges_by_index


def test_p2_crossing_relationships_and_helpers() -> None:
    """Verify geometric crossing detection between horizontal and vertical bridges."""
    puzzle, bridges = _p2_crossing_fixture()
    # Sorted islands: T(0,1), L(1,0), R(1,3), B(2,1)
    # E1 (idx 0): T -> B (vertical, col 1, rows 0..2)
    # E2 (idx 1): L -> R (horizontal, row 1, cols 0..3)
    assert [(b["id"], b["from"], b["to"], b["orientation"]) for b in bridges] == [
        ("E1", "T", "B", "vertical"),
        ("E2", "L", "R", "horizontal"),
    ]

    ctx = build_graph_context(puzzle, bridges)

    assert ctx.crossing_edges_by_index == {
        0: [1],
        1: [0],
    }
    assert ctx.would_edges_cross(0, 1) is True
    assert ctx.would_edges_cross(1, 0) is True
    assert ctx.would_edges_cross(0, 0) is False
    assert ctx.get_crossing_edges(0) == [1]
    assert ctx.get_incident_edges("T") == [0]
    assert ctx.get_incident_edges("L") == [1]


def test_irregular_grid_and_isolated_island() -> None:
    """Verify irregular grids, non-skipping nearest-island rule, and isolated islands."""
    puzzle, bridges = _irregular_grid_fixture()
    # Sorted islands: I1(0,0), I2(0,2), I3(0,4), I4(2,0), ISO(3,4)
    # E1 (idx 0): I1 -> I2 (horizontal)  [skips nothing; I2 is nearest right]
    # E2 (idx 1): I1 -> I4 (vertical)
    # E3 (idx 2): I2 -> I3 (horizontal)  [I1 does NOT link directly to I3]
    # E4 (idx 3): I3 -> ISO (vertical)
    assert [(b["id"], b["from"], b["to"]) for b in bridges] == [
        ("E1", "I1", "I2"),
        ("E2", "I1", "I4"),
        ("E3", "I2", "I3"),
        ("E4", "I3", "ISO"),
    ]

    ctx = build_graph_context(puzzle, bridges)

    assert ctx.incident_edges_by_island == {
        "I1": [0, 1],
        "I2": [0, 2],
        "I3": [2, 3],
        "I4": [1],
        "ISO": [3],
    }
    assert ctx.crossing_edges_by_index == {0: [], 1: [], 2: [], 3: []}
    assert ctx.max_possible_degree("I4") == 2
    assert ctx.get_incident_edges("NON_EXISTENT") == []


def test_candidate_bridges_order_and_ids_not_mutated() -> None:
    """Ensure build_graph_context never reorders or mutates candidate_bridges."""
    puzzle, bridges = _p1_fixture()
    snapshot = copy.deepcopy(bridges)

    ctx = build_graph_context(puzzle, bridges)

    assert bridges == snapshot
    assert ctx.candidate_bridges == snapshot
    assert [b["id"] for b in ctx.candidate_bridges] == ["E1", "E2", "E3", "E4"]


def test_graph_context_getters_do_not_expose_internal_lists() -> None:
    """Verify getter methods return copies, not internal lists."""
    puzzle, bridges = _p2_crossing_fixture()
    ctx = build_graph_context(puzzle, bridges)

    # Test incident edges getter
    incident_edges = ctx.get_incident_edges("T")
    incident_edges.clear()

    assert ctx.get_incident_edges("T") == [0]

    # Test crossing edges getter
    crossing_edges = ctx.get_crossing_edges(0)
    crossing_edges.clear()

    assert ctx.get_crossing_edges(0) == [1]