"""S1-03 tests (owner: Monzer). Remove the xfail marker below once the module is implemented."""
import random

import pytest

from core.candidate_generator import generate_candidate_edges
from tests.helpers import P1_ISLANDS, P2_ISLANDS, isl

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="S1-03 not implemented yet - delete this marker when done",
)


def triples(edges):
    return [(e["from"], e["to"], e["orientation"]) for e in edges]


def test_two_islands_same_row():
    edges = generate_candidate_edges([isl("A", 0, 0, 1), isl("B", 0, 3, 1)])
    assert triples(edges) == [("A", "B", "horizontal")]
    assert [e["id"] for e in edges] == ["E1"]


def test_two_islands_same_column():
    edges = generate_candidate_edges([isl("A", 0, 0, 1), isl("B", 4, 0, 1)])
    assert triples(edges) == [("A", "B", "vertical")]


def test_three_in_a_row_no_link_over_the_middle_island():
    islands = [isl("A", 0, 0, 1), isl("B", 0, 2, 2), isl("C", 0, 4, 1)]
    edges = generate_candidate_edges(islands)
    assert triples(edges) == [("A", "B", "horizontal"), ("B", "C", "horizontal")]


def test_islands_not_sharing_row_or_column():
    assert generate_candidate_edges([isl("A", 0, 0, 1), isl("B", 1, 1, 1)]) == []


def test_single_island():
    assert generate_candidate_edges([isl("A", 0, 0, 1)]) == []


def test_p1_exact_edges_and_order():
    edges = generate_candidate_edges(P1_ISLANDS)
    assert [e["id"] for e in edges] == ["E1", "E2", "E3", "E4"]
    assert triples(edges) == [
        ("A", "B", "horizontal"),
        ("A", "C", "vertical"),
        ("B", "D", "vertical"),
        ("C", "D", "horizontal"),
    ]


def test_p2_exact_edges_and_order():
    edges = generate_candidate_edges(P2_ISLANDS)
    assert [e["id"] for e in edges] == ["E1", "E2"]
    assert triples(edges) == [("C", "D", "vertical"), ("A", "B", "horizontal")]


def test_input_order_does_not_change_result():
    expected = generate_candidate_edges(P1_ISLANDS)
    for seed in range(5):
        shuffled = list(P1_ISLANDS)
        random.Random(seed).shuffle(shuffled)
        assert generate_candidate_edges(shuffled) == expected
