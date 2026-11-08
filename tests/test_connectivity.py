"""S1-06 tests (owner: Ebrahim). Remove the xfail marker below once the module is implemented."""
import pytest

from core.connectivity_checker import find_connected_components, is_connected
from tests.helpers import P1_EDGES, P1_ISLANDS, component_set, isl, p1

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="S1-06 not implemented yet - delete this marker when done",
)


def comps(values):
    return component_set(find_connected_components(P1_ISLANDS, P1_EDGES, p1(values)))


def fs(*ids):
    return frozenset(ids)


def test_fully_connected():
    assert comps([1, 1, 1, 1]) == {fs("A", "B", "C", "D")}
    assert is_connected(P1_ISLANDS, P1_EDGES, p1([1, 1, 1, 1])) is True


def test_split_ab_cd():
    assert comps([2, 0, 0, 2]) == {fs("A", "B"), fs("C", "D")}
    assert is_connected(P1_ISLANDS, P1_EDGES, p1([2, 0, 0, 2])) is False


def test_split_ac_bd():
    assert comps([0, 2, 2, 0]) == {fs("A", "C"), fs("B", "D")}


def test_one_isolated_island():
    assert comps([1, 1, 0, 0]) == {fs("A", "B", "C"), fs("D")}


def test_no_bridges_every_island_alone():
    assert comps([0, 0, 0, 0]) == {fs("A"), fs("B"), fs("C"), fs("D")}


def test_single_island_is_connected():
    islands = [isl("A", 0, 0, 1)]
    assert find_connected_components(islands, [], {"bridge_counts": {}}) == [["A"]]
    assert is_connected(islands, [], {"bridge_counts": {}}) is True


def test_double_bridge_is_one_connection():
    assert len(find_connected_components(P1_ISLANDS, P1_EDGES, p1([2, 0, 0, 2]))) == 2


def test_candidate_edge_with_zero_count_is_not_a_connection():
    assert len(find_connected_components(P1_ISLANDS, P1_EDGES, p1([0, 0, 0, 0]))) == 4
