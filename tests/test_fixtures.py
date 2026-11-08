"""Sanity checks for the shared fixtures (always run, never xfail)."""
from tests.helpers import P1_EDGES, P1_ISLANDS, P2_EDGES, P2_ISLANDS, p1


def test_p1_required_sum_is_even():
    assert sum(i["required_bridges"] for i in P1_ISLANDS) % 2 == 0


def test_p1_known_solution_degrees_by_hand():
    sol = p1([1, 1, 1, 1])["bridge_counts"]
    degree = {i["id"]: 0 for i in P1_ISLANDS}
    for e in P1_EDGES:
        degree[e["from"]] += sol[e["id"]]
        degree[e["to"]] += sol[e["id"]]
    assert degree == {"A": 2, "B": 2, "C": 2, "D": 2}


def test_edge_ids_are_sequential():
    assert [e["id"] for e in P1_EDGES] == ["E1", "E2", "E3", "E4"]
    assert [e["id"] for e in P2_EDGES] == ["E1", "E2"]
    assert len(P2_ISLANDS) == 4
