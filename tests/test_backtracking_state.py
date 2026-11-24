import pytest

from core.backtracking_state import BacktrackingState
from tests.helpers import P1_EDGES, P1_ISLANDS


def snapshot(state):
    return (
        state.assignments.copy(),
        state.current_degree.copy(),
        state.remaining_capacity.copy(),
    )


def test_initial_state_uses_none_and_capacity_two_per_candidate():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)

    assert state.assignments == [None, None, None, None]
    assert state.current_degree == {"A": 0, "B": 0, "C": 0, "D": 0}
    assert state.remaining_capacity == {"A": 4, "B": 4, "C": 4, "D": 4}
    assert state.is_feasible()


def test_zero_is_explicit_assignment_and_reduces_capacity():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)
    state.assign(0, 0)

    assert state.assignments[0] == 0
    assert state.current_degree["A"] == 0
    assert state.current_degree["B"] == 0
    assert state.remaining_capacity["A"] == 2
    assert state.remaining_capacity["B"] == 2

    with pytest.raises(ValueError):
        state.assign(0, 1)


def test_assign_updates_both_endpoints_and_undo_restores_state():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)
    before = snapshot(state)

    state.assign(0, 2)

    assert state.current_degree["A"] == 2
    assert state.current_degree["B"] == 2
    assert state.remaining_capacity["A"] == 2
    assert state.remaining_capacity["B"] == 2

    state.undo(0, 2)

    assert snapshot(state) == before


def test_multi_level_assign_and_rollback_restores_exact_state():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)
    before = snapshot(state)
    decisions = [(0, 1), (1, 0), (2, 2), (3, 1)]

    for candidate_idx, count in decisions:
        state.assign(candidate_idx, count)

    for candidate_idx, count in reversed(decisions):
        state.undo(candidate_idx, count)

    assert snapshot(state) == before


def test_infeasible_when_island_cannot_reach_required_degree():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)
    state.assign(0, 0)
    state.assign(1, 0)

    assert not state.is_feasible()


def test_rejects_invalid_assignment_and_mismatched_undo():
    state = BacktrackingState(P1_ISLANDS, P1_EDGES)

    with pytest.raises(ValueError):
        state.assign(0, True)

    with pytest.raises(ValueError):
        state.assign(0, 3)

    state.assign(0, 1)

    with pytest.raises(ValueError):
        state.undo(0, 2)