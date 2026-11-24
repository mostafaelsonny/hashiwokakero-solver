"""Tests for Unified Algorithm Runner (Sprint 2 - S2-12).

Verifies the central execution gateway, defensive input validation,
algorithm dispatch (Backtracking, GA, MA), and independent validation safeguards.
"""
from __future__ import annotations

from typing import Any, Dict
from unittest.mock import patch

import pytest

from core.algorithm_runner import (
    list_supported_algorithms,
    normalize_algorithm_name,
    run_algorithm,
    validate_puzzle_structure,
)
from tests.helpers import P1_EDGES, P1_PUZZLE, P2_EDGES, P2_PUZZLE

IMPOSSIBLE_PUZZLE = {
    "rows": 1,
    "cols": 3,
    "islands": [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 5},
        {"id": "B", "row": 0, "col": 2, "required_bridges": 5},
    ],
}


# ==============================================================================
# 1. Algorithm Name Normalization & Supported List
# ==============================================================================
def test_list_supported_algorithms():
    algos = list_supported_algorithms()
    assert "backtracking" in algos
    assert "genetic" in algos
    assert "memetic" in algos


@pytest.mark.parametrize(
    "raw,expected",
    [
        ("backtracking", "backtracking"),
        ("Backtracking", "backtracking"),
        ("  bt  ", "backtracking"),
        ("BT", "backtracking"),
        ("genetic", "genetic"),
        ("GA", "genetic"),
        ("  ga  ", "genetic"),
        ("memetic", "memetic"),
        ("MA", "memetic"),
        ("  Memetic  ", "memetic"),
    ],
)
def test_normalize_algorithm_name_valid(raw, expected):
    assert normalize_algorithm_name(raw) == expected


@pytest.mark.parametrize("invalid", ["unknown", "dfs", "astar", "", None, 123, []])
def test_normalize_algorithm_name_invalid(invalid):
    assert normalize_algorithm_name(invalid) is None


def test_unsupported_algorithm_returns_invalid_input():
    result = run_algorithm(P1_PUZZLE, "unsupported_solver")
    assert result["status"] == "INVALID_INPUT"
    assert result["solution"] is None
    assert result["validation_report"] is None
    assert "error" in result["metrics"]
    assert "Unsupported algorithm" in result["metrics"]["error"]


# ==============================================================================
# 2. Defensive Puzzle & Config Input Validation
# ==============================================================================
def test_validate_valid_puzzle():
    valid, err = validate_puzzle_structure(P1_PUZZLE)
    assert valid is True
    assert err is None


@pytest.mark.parametrize(
    "bad_puzzle,expected_err",
    [
        ("not_a_dict", "must be a dictionary"),
        ({"rows": 0, "cols": 3, "islands": []}, "rows must be an integer >= 1"),
        ({"rows": 3, "cols": -1, "islands": []}, "cols must be an integer >= 1"),
        ({"rows": 3, "cols": 3, "islands": "not_a_list"}, "islands must be a list"),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [{"id": "", "row": 0, "col": 0, "required_bridges": 1}],
            },
            "invalid id",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [
                    {"id": "A", "row": 0, "col": 0, "required_bridges": 1},
                    {"id": "A", "row": 1, "col": 1, "required_bridges": 1},
                ],
            },
            "Duplicate island id",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [
                    {"id": "A", "row": 0, "col": 0, "required_bridges": 1},
                    {"id": "B", "row": 0, "col": 0, "required_bridges": 1},
                ],
            },
            "Duplicate island coordinate",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [{"id": "A", "row": 5, "col": 0, "required_bridges": 1}],
            },
            "row out of bounds",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [{"id": "A", "row": 0, "col": 4, "required_bridges": 1}],
            },
            "col out of bounds",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [{"id": "A", "row": 0, "col": 0, "required_bridges": 9}],
            },
            "required_bridges must be in [1, 8]",
        ),
        (
            {
                "rows": 3,
                "cols": 3,
                "islands": [{"id": "A", "row": 0, "col": 0, "required_bridges": 0}],
            },
            "required_bridges must be in [1, 8]",
        ),
    ],
)
def test_validate_invalid_puzzles(bad_puzzle, expected_err):
    valid, err = validate_puzzle_structure(bad_puzzle)
    assert valid is False
    assert expected_err in err

    result = run_algorithm(bad_puzzle, "backtracking")
    assert result["status"] == "INVALID_INPUT"
    assert result["solution"] is None
    assert expected_err in result["metrics"]["error"]


def test_invalid_config_type_returns_invalid_input():
    result = run_algorithm(P1_PUZZLE, "backtracking", config="not_a_dict")  # type: ignore
    assert result["status"] == "INVALID_INPUT"
    assert "config must be a dictionary" in result["metrics"]["error"]


# ==============================================================================
# 3. Solver Execution & Dispatch (Backtracking, GA, MA)
# ==============================================================================
def test_run_algorithm_backtracking_p1():
    result = run_algorithm(P1_PUZZLE, "backtracking")
    assert result["status"] == "SOLVED"
    assert result["solution"] == {"bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}}
    assert result["validation_report"] is not None
    assert result["validation_report"]["valid"] is True
    metrics = result["metrics"]
    assert metrics["algorithm"] == "backtracking"
    assert metrics["runtime_ms"] > 0.0
    assert "explored_states" in metrics


def test_run_algorithm_backtracking_alias_bt():
    result = run_algorithm(P1_PUZZLE, "bt")
    assert result["status"] == "SOLVED"
    assert result["metrics"]["algorithm"] == "backtracking"


def test_run_algorithm_backtracking_unsatisfiable():
    result = run_algorithm(IMPOSSIBLE_PUZZLE, "backtracking")
    assert result["status"] == "UNSATISFIABLE"
    assert result["solution"] is None
    assert result["validation_report"] is None


def test_run_algorithm_backtracking_limit_reached():
    result = run_algorithm(P1_PUZZLE, "backtracking", config={"max_states": 1})
    assert result["status"] == "LIMIT_REACHED"
    assert result["solution"] is None


def test_run_algorithm_genetic_p1():
    result = run_algorithm(
        P1_PUZZLE, "ga", config={"population_size": 40, "max_generations": 30, "seed": 42}
    )
    assert result["status"] == "SOLVED"
    assert result["solution"] == {"bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}}
    assert result["validation_report"]["valid"] is True
    assert result["metrics"]["algorithm"] == "genetic"
    assert result["metrics"]["generations"] >= 0


def test_run_algorithm_genetic_impossible_bounded():
    result = run_algorithm(
        IMPOSSIBLE_PUZZLE, "genetic", config={"population_size": 10, "max_generations": 5, "seed": 99}
    )
    assert result["status"] == "NO_VALID_SOLUTION_FOUND"
    assert result["solution"] is None


def test_run_algorithm_memetic_p1():
    result = run_algorithm(
        P1_PUZZLE, "ma", config={"population_size": 40, "max_generations": 30, "seed": 42}
    )
    assert result["status"] == "SOLVED"
    assert result["solution"] == {"bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}}
    assert result["validation_report"]["valid"] is True
    assert result["metrics"]["algorithm"] == "memetic"
    assert result["metrics"]["local_search_calls"] >= 0


def test_run_algorithm_memetic_impossible_bounded():
    result = run_algorithm(
        IMPOSSIBLE_PUZZLE, "memetic", config={"population_size": 10, "max_generations": 5, "seed": 99}
    )
    assert result["status"] == "NO_VALID_SOLUTION_FOUND"
    assert result["solution"] is None


# ==============================================================================
# 4. Independent Validation Safeguard
# ==============================================================================
def test_independent_validation_safeguard_overrides_invalid_claimed_solution():
    """If a rogue or buggy solver claims 'SOLVED' with an invalid solution,

    the runner MUST catch it independently, override status to INVALID_RESULT,
    and report the exact validation violations.
    """
    fake_bad_solution = {"bridge_counts": {"E1": 2, "E2": 0, "E3": 0, "E4": 0}}

    def mock_bad_solver(puzzle, candidate_bridges, config=None):
        return {
            "status": "SOLVED",
            "solution": fake_bad_solution,
            "validation_report": {"valid": True},  # Falsely claims valid
            "metrics": {"explored_states": 1},
        }

    with patch("core.algorithm_runner.solve_backtracking", side_effect=mock_bad_solver):
        result = run_algorithm(P1_PUZZLE, "backtracking")
        assert result["status"] == "INVALID_RESULT"
        assert result["validation_report"] is not None
        assert result["validation_report"]["valid"] is False
        assert len(result["validation_report"]["degree_violations"]) > 0
        assert "validation_error" in result["metrics"]


def test_independent_validation_safeguard_catches_missing_solution_dictionary():
    def mock_missing_solution(puzzle, candidate_bridges, config=None):
        return {
            "status": "SOLVED",
            "solution": None,  # Missing solution
            "validation_report": None,
            "metrics": {},
        }

    with patch("core.algorithm_runner.solve_backtracking", side_effect=mock_missing_solution):
        result = run_algorithm(P1_PUZZLE, "backtracking")
        assert result["status"] == "INVALID_RESULT"
        assert result["solution"] is None
        assert "missing or invalid" in result["metrics"]["validation_error"]
