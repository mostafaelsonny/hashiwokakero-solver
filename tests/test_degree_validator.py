"""S1-04 tests (owner: Ebrahim). Remove the xfail marker below once the module is implemented."""
import pytest

from core.degree_validator import check_degrees, compute_degrees
from tests.helpers import P1_EDGES, P1_ISLANDS, p1

pytestmark = pytest.mark.xfail(
    raises=NotImplementedError,
    reason="S1-04 not implemented yet - delete this marker when done",
)


def check(values, mode):
    result = check_degrees(P1_ISLANDS, P1_EDGES, p1(values), mode)
    return sorted(result, key=lambda v: v["island"])


def v(island, required, actual):
    return {"island": island, "required": required, "actual": actual}


def test_compute_degrees_counts_double_bridge_twice():
    degrees = compute_degrees(P1_ISLANDS, P1_EDGES, p1([2, 2, 0, 0]))
    assert degrees == {"A": 4, "B": 2, "C": 2, "D": 0}


def test_valid_solution_passes_both_modes():
    assert check([1, 1, 1, 1], "partial") == []
    assert check([1, 1, 1, 1], "final") == []


def test_missing_bridges_final_only():
    assert check([1, 0, 1, 1], "partial") == []
    assert check([1, 0, 1, 1], "final") == [v("A", 2, 1), v("C", 2, 1)]


def test_too_many_bridges_fails_partial_and_final():
    assert check([2, 2, 0, 0], "partial") == [v("A", 2, 4)]
    assert check([2, 2, 0, 0], "final") == [v("A", 2, 4), v("D", 2, 0)]


def test_degree_ok_even_if_network_is_split():
    assert check([2, 0, 0, 2], "partial") == []
    assert check([2, 0, 0, 2], "final") == []


def test_no_bridges_at_all():
    assert check([0, 0, 0, 0], "partial") == []
    assert len(check([0, 0, 0, 0], "final")) == 4


def test_invalid_bridge_value_raises():
    with pytest.raises(ValueError):
        check_degrees(P1_ISLANDS, P1_EDGES, p1([3, 0, 0, 0]), "final")


def test_unknown_mode_raises():
    with pytest.raises(ValueError):
        check_degrees(P1_ISLANDS, P1_EDGES, p1([1, 1, 1, 1]), "whatever")
