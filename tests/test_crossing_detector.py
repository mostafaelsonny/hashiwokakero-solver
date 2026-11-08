"""S1-05 tests (owner: Monzer). Remove the xfail marker below once the module is implemented."""
import pytest

from core.crossing_detector import detect_crossings, get_crossing_pairs
from tests.helpers import (
    P1_EDGES,
    P1_ISLANDS,
    P2_EDGES,
    P2_ISLANDS,
    edge,
    isl,
    make_solution,
    p1,
    p2,
    pair_set,
)

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="S1-05 not implemented yet - delete this marker when done",
)

CROSS = {frozenset({"E1", "E2"})}


def crossings(values):
    return pair_set(detect_crossings(P2_ISLANDS, P2_EDGES, p2(values)))


def test_p2_both_bridges_cross():
    assert crossings([1, 1]) == CROSS


def test_p2_double_bridges_are_still_one_crossing():
    result = detect_crossings(P2_ISLANDS, P2_EDGES, p2([2, 2]))
    assert len(result) == 1
    assert pair_set(result) == CROSS


def test_p2_zero_count_edge_is_not_a_bridge():
    assert crossings([1, 0]) == set()
    assert crossings([0, 1]) == set()


def test_p2_no_bridges():
    assert crossings([0, 0]) == set()


def test_potential_crossing_pairs_p2():
    assert pair_set(get_crossing_pairs(P2_ISLANDS, P2_EDGES)) == CROSS


def test_p1_bridges_meeting_at_islands_do_not_cross():
    assert detect_crossings(P1_ISLANDS, P1_EDGES, p1([1, 1, 1, 1])) == []


def test_potential_crossing_pairs_p1_empty():
    assert get_crossing_pairs(P1_ISLANDS, P1_EDGES) == []


def test_horizontal_chain_has_no_crossings():
    islands = [isl("A", 0, 0, 1), isl("B", 0, 2, 2), isl("C", 0, 4, 2), isl("D", 0, 6, 1)]
    edges = [
        edge("E1", "A", "B", "horizontal"),
        edge("E2", "B", "C", "horizontal"),
        edge("E3", "C", "D", "horizontal"),
    ]
    assert detect_crossings(islands, edges, make_solution([1, 1, 1], edges)) == []
