"""S1-07 tests (owner: Ebrahim). Remove the xfail marker below once the module is implemented."""
import pytest

from core.solution_validator import validate_solution
from tests.helpers import P1_PUZZLE, P2_PUZZLE, p1, p2, pair_set

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="S1-07 not implemented yet - delete this marker when done",
)


def test_known_valid_solution():
    report = validate_solution(P1_PUZZLE, p1([1, 1, 1, 1]))
    assert report["valid"] is True
    assert report["degree_violations"] == []
    assert report["crossings"] == []
    assert report["connected_components"] == 1
    assert report["invalid_values"] == []


def test_degree_violations_are_reported():
    report = validate_solution(P1_PUZZLE, p1([1, 0, 1, 1]))
    assert report["valid"] is False
    violations = sorted(report["degree_violations"], key=lambda v: v["island"])
    assert violations == [
        {"island": "A", "required": 2, "actual": 1},
        {"island": "C", "required": 2, "actual": 1},
    ]
    assert report["crossings"] == []
    assert report["connected_components"] == 1


def test_degree_ok_but_network_split():
    for values in ([2, 0, 0, 2], [0, 2, 2, 0]):
        report = validate_solution(P1_PUZZLE, p1(values))
        assert report["valid"] is False
        assert report["degree_violations"] == []
        assert report["connected_components"] == 2


def test_crossing_is_reported():
    report = validate_solution(P2_PUZZLE, p2([1, 1]))
    assert report["valid"] is False
    assert pair_set(report["crossings"]) == {frozenset({"E1", "E2"})}


def test_invalid_bridge_value_is_reported_without_crashing():
    report = validate_solution(P1_PUZZLE, {"bridge_counts": {"E1": 3, "E2": 1, "E3": 1, "E4": 1}})
    assert report["valid"] is False
    assert any(item["edge"] == "E1" for item in report["invalid_values"])


def test_unknown_edge_id_is_reported():
    report = validate_solution(P1_PUZZLE, {"bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1, "E9": 1}})
    assert report["valid"] is False
    assert any(item["edge"] == "E9" for item in report["invalid_values"])


def test_missing_edge_ids_count_as_zero():
    report = validate_solution(P1_PUZZLE, {"bridge_counts": {}})
    assert report["valid"] is False
    assert len(report["degree_violations"]) == 4
    assert report["invalid_values"] == []


def test_all_problems_reported_together():
    report = validate_solution(P1_PUZZLE, p1([2, 2, 0, 0]))
    assert report["valid"] is False
    assert {v["island"] for v in report["degree_violations"]} == {"A", "D"}
    assert report["connected_components"] == 2
