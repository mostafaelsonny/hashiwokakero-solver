from copy import deepcopy

import core.backtracking_solver as solver_module
from core.backtracking_state import BacktrackingState
from core.candidate_generator import generate_candidate_edges
from core.solution_validator import validate_solution
from tests.helpers import P1_ISLANDS, P1_PUZZLE, P2_PUZZLE


def solve(puzzle, config=None):
    candidates = generate_candidate_edges(puzzle["islands"])
    return solver_module.solve_backtracking(puzzle, candidates, config)


def test_solves_p1_and_returns_canonical_solution():
    result = solve(P1_PUZZLE)

    assert result["status"] == "SOLVED"
    assert result["solution"] == {
        "bridge_counts": {
            "E1": 1,
            "E2": 1,
            "E3": 1,
            "E4": 1,
        }
    }
    assert result["validation_report"]["valid"] is True


def test_degree_complete_but_disconnected_assignment_is_rejected(monkeypatch):
    disconnected = {
        "bridge_counts": {
            "E1": 2,
            "E2": 0,
            "E3": 0,
            "E4": 2,
        }
    }

    # تأكيد أن درجات الجزر صحيحة رغم أن الشبكة مقسومة لمكوّنين.
    report = validate_solution(P1_PUZZLE, disconnected)
    assert report["degree_violations"] == []
    assert report["connected_components"] == 2
    assert report["valid"] is False

    # سجّل الحلول الكاملة التي مررها الـsolver للـvalidator.
    original_validator = solver_module.validate_solution
    checked_solutions = []

    def recording_validator(puzzle, solution):
        result = original_validator(puzzle, solution)
        checked_solutions.append((deepcopy(solution), result))
        return result

    monkeypatch.setattr(
        solver_module,
        "validate_solution",
        recording_validator,
    )

    # هذا الترتيب يجعل البحث يصل إلى [2, 0, 0, 2] ويرفضه،
    # ثم يكمل حتى يجد حل P1 المتصل.
    result = solve(P1_PUZZLE, {"value_order": [2, 0, 1]})

    assert any(
        solution == disconnected
        and checked["valid"] is False
        and checked["connected_components"] == 2
        for solution, checked in checked_solutions
    )
    assert result["status"] == "SOLVED"
    assert result["validation_report"]["valid"] is True


def test_solver_accepts_a_double_bridge_solution():
    puzzle = {
        "rows": 1,
        "cols": 3,
        "islands": [
            {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
            {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
        ],
    }

    result = solve(puzzle)

    assert result["status"] == "SOLVED"
    assert result["solution"] == {
        "bridge_counts": {"E1": 2}
    }
    assert result["validation_report"]["valid"] is True


def test_crossing_candidates_are_pruned():
    result = solve(P2_PUZZLE)

    assert result["status"] == "UNSATISFIABLE"
    assert result["metrics"]["pruned_crossing"] > 0


def test_returns_unsatisfiable_when_search_is_exhausted():
    puzzle = {
        "rows": 1,
        "cols": 1,
        "islands": [
            {"id": "A", "row": 0, "col": 0, "required_bridges": 1},
        ],
    }

    result = solve(puzzle)

    assert result["status"] == "UNSATISFIABLE"
    assert result["solution"] is None
    assert result["validation_report"] is None


def test_returns_limit_reached_when_state_budget_is_exhausted():
    result = solve(P1_PUZZLE, {"max_states": 1})

    assert result["status"] == "LIMIT_REACHED"
    assert result["solution"] is None
    assert result["validation_report"] is None
    assert result["metrics"]["explored_states"] == 1


def test_upper_degree_pruning_is_active():
    result = solve(P1_PUZZLE, {"value_order": [2, 1, 0]})

    assert result["status"] == "SOLVED"
    assert result["metrics"]["pruned_degree_upper"] > 0


def test_lower_capacity_pruning_is_active():
    result = solve(P1_PUZZLE, {"value_order": [0, 1, 2]})

    assert result["status"] == "SOLVED"
    assert result["metrics"]["pruned_degree_lower"] > 0


def test_solver_does_not_mutate_candidate_list():
    candidates = generate_candidate_edges(P1_ISLANDS)
    original = deepcopy(candidates)

    result = solver_module.solve_backtracking(P1_PUZZLE, candidates)

    assert result["status"] == "SOLVED"
    assert candidates == original


def test_invalid_config_returns_standard_result():
    result = solve(P1_PUZZLE, {"value_order": [0, 0, 2]})

    assert result["status"] == "INVALID_INPUT"
    assert result["solution"] is None
    assert result["validation_report"] is None
    assert "error" in result["metrics"]


def test_result_has_standard_contract_fields_and_metrics():
    result = solve(P1_PUZZLE)

    assert set(result) == {
        "status",
        "solution",
        "validation_report",
        "metrics",
    }
    assert result["status"] in {
        "SOLVED",
        "UNSATISFIABLE",
        "LIMIT_REACHED",
        "INVALID_INPUT",
    }

    metrics = result["metrics"]
    assert isinstance(metrics["runtime_ms"], float)
    assert metrics["runtime_ms"] >= 0
    assert isinstance(metrics["explored_states"], int)
    assert metrics["explored_states"] > 0
    assert isinstance(metrics["backtracks"], int)


def test_invalid_input_does_not_raise_to_caller():
    candidates = generate_candidate_edges(P1_ISLANDS)
    candidates[0]["from"] = "UNKNOWN"

    result = solver_module.solve_backtracking(P1_PUZZLE, candidates)

    assert result["status"] == "INVALID_INPUT"
    assert result["solution"] is None
    assert result["validation_report"] is None


def test_state_is_restored_after_exhausting_failed_branches(monkeypatch):
    created_states = []

    class CapturingBacktrackingState(BacktrackingState):
        def __init__(self, islands, candidates):
            super().__init__(islands, candidates)
            created_states.append(self)

    monkeypatch.setattr(
        solver_module,
        "BacktrackingState",
        CapturingBacktrackingState,
    )

    result = solve(P2_PUZZLE)

    assert result["status"] == "UNSATISFIABLE"
    assert len(created_states) == 1

    state = created_states[0]
    assert state.assignments == [None, None]
    assert state.current_degree == {
        "A": 0,
        "B": 0,
        "C": 0,
        "D": 0,
    }
    assert state.remaining_capacity == {
        "A": 2,
        "B": 2,
        "C": 2,
        "D": 2,
    }