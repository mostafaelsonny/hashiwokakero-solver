"""Unified Algorithm Runner (Sprint 2 - S2-12).

Serves as the central execution pipeline and integration engine for all Hashiwokakero solvers:
  1. Validates input puzzle structures defensively.
  2. Generates canonical candidate bridges (E1..En) exactly once.
  3. Dispatches execution to the requested algorithm (Backtracking, GA, MA).
  4. Applies an independent final validation safeguard (core.solution_validator.validate_solution).
  5. Returns standardized SolverResult conforming to docs/ALGORITHM_INTERFACE.md.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Set, Tuple

from algorithms.ga.genetic_solver import solve_genetic
from algorithms.ma.memetic_solver import solve_memetic
from core.backtracking_solver import solve_backtracking
from core.candidate_generator import generate_candidate_edges
from core.models import Puzzle, SolverResult
from core.solution_validator import validate_solution

SUPPORTED_ALGORITHMS: Tuple[str, ...] = ("backtracking", "genetic", "memetic")

_ALGORITHM_ALIASES: Dict[str, str] = {
    "backtracking": "backtracking",
    "bt": "backtracking",
    "genetic": "genetic",
    "ga": "genetic",
    "memetic": "memetic",
    "ma": "memetic",
}


def list_supported_algorithms() -> List[str]:
    """Return the list of canonical supported algorithm names."""
    return list(SUPPORTED_ALGORITHMS)


def normalize_algorithm_name(name: Any) -> Optional[str]:
    """Normalize and resolve algorithm name aliases.

    Supported inputs (case-insensitive):
      - 'backtracking', 'bt' -> 'backtracking'
      - 'genetic', 'ga' -> 'genetic'
      - 'memetic', 'ma' -> 'memetic'

    Returns canonical name or None if unrecognized.
    """
    if not isinstance(name, str):
        return None
    cleaned = name.strip().lower()
    return _ALGORITHM_ALIASES.get(cleaned)


def validate_puzzle_structure(puzzle: Any) -> Tuple[bool, Optional[str]]:
    """Defensively validate puzzle dictionary against docs/DATA_MODEL.md constraints.

    Returns:
        (is_valid, error_message_if_invalid)
    """
    if not isinstance(puzzle, dict):
        return False, f"Puzzle must be a dictionary, got {type(puzzle).__name__}"

    rows = puzzle.get("rows")
    cols = puzzle.get("cols")
    islands = puzzle.get("islands")

    if type(rows) is not int or rows < 1:
        return False, f"rows must be an integer >= 1, got {rows!r}"

    if type(cols) is not int or cols < 1:
        return False, f"cols must be an integer >= 1, got {cols!r}"

    if not isinstance(islands, list):
        return False, f"islands must be a list, got {type(islands).__name__}"

    seen_ids: Set[str] = set()
    seen_coords: Set[Tuple[int, int]] = set()

    for idx, island in enumerate(islands):
        if not isinstance(island, dict):
            return False, f"Island at index {idx} must be a dictionary"

        isl_id = island.get("id")
        row = island.get("row")
        col = island.get("col")
        req = island.get("required_bridges")

        if not isinstance(isl_id, str) or not isl_id.strip():
            return False, f"Island at index {idx} has invalid id: {isl_id!r}"

        if isl_id in seen_ids:
            return False, f"Duplicate island id: {isl_id!r}"
        seen_ids.add(isl_id)

        if type(row) is not int or not (0 <= row < rows):
            return False, f"Island {isl_id!r} row out of bounds: {row!r} for rows={rows}"

        if type(col) is not int or not (0 <= col < cols):
            return False, f"Island {isl_id!r} col out of bounds: {col!r} for cols={cols}"

        coord = (row, col)
        if coord in seen_coords:
            return False, f"Duplicate island coordinate {coord} for island {isl_id!r}"
        seen_coords.add(coord)

        if type(req) is not int or not (1 <= req <= 8):
            return False, f"Island {isl_id!r} required_bridges must be in [1, 8], got {req!r}"

    return True, None


def run_algorithm(
    puzzle: Puzzle,
    algorithm_name: str,
    config: Optional[Dict[str, Any]] = None,
) -> SolverResult:
    """Central gateway for executing any solver algorithm with independent validation.

    Execution Pipeline:
      1. Validate input puzzle structure & algorithm name.
      2. Generate canonical candidate bridges (E1..En) once.
      3. Dispatch to selected solver (Backtracking, GA, or MA).
      4. Apply independent final validation safeguard (validate_solution).
      5. Return standardized SolverResult dictionary.

    Args:
        puzzle: Puzzle dictionary adhering to DATA_MODEL.md.
        algorithm_name: 'backtracking' ('bt') | 'genetic' ('ga') | 'memetic' ('ma').
        config: Optional solver-specific hyperparameters dictionary.

    Returns:
        Standard SolverResult:
        {
            "status": "SOLVED" | "UNSATISFIABLE" | "LIMIT_REACHED" |
                      "NO_VALID_SOLUTION_FOUND" | "INVALID_INPUT" | "INVALID_RESULT",
            "solution": Solution | None,
            "validation_report": ValidationReport | None,
            "metrics": dict,
        }
    """
    start_time = time.perf_counter()

    # 1. Validate Algorithm Name
    canonical_algo = normalize_algorithm_name(algorithm_name)
    if canonical_algo is None:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        supported = list_supported_algorithms()
        return {
            "status": "INVALID_INPUT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": elapsed_ms,
                "error": f"Unsupported algorithm {algorithm_name!r}. Supported algorithms: {supported}",
            },
        }

    # 2. Validate Config Type
    if config is not None and not isinstance(config, dict):
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "INVALID_INPUT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": elapsed_ms,
                "error": f"config must be a dictionary or None, got {type(config).__name__}",
            },
        }

    # 3. Validate Puzzle Input
    is_valid_puzzle, error_msg = validate_puzzle_structure(puzzle)
    if not is_valid_puzzle:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "INVALID_INPUT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": elapsed_ms,
                "error": error_msg or "Invalid puzzle structure",
            },
        }

    # 4. Generate Candidate Bridges Once
    try:
        candidate_bridges = generate_candidate_edges(puzzle["islands"])
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "INVALID_INPUT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": elapsed_ms,
                "error": f"Failed generating candidate bridges: {exc}",
            },
        }

    # 5. Dispatch to Selected Solver
    try:
        if canonical_algo == "backtracking":
            result = solve_backtracking(puzzle, candidate_bridges, config=config)
        elif canonical_algo == "genetic":
            result = solve_genetic(puzzle, candidate_bridges, config=config)
        elif canonical_algo == "memetic":
            result = solve_memetic(puzzle, candidate_bridges, config=config)
        else:
            raise ValueError(f"Unhandled algorithm: {canonical_algo}")
    except Exception as exc:
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        return {
            "status": "INVALID_INPUT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": elapsed_ms,
                "algorithm": canonical_algo,
                "error": f"Unhandled solver exception: {exc}",
            },
        }

    total_runtime_ms = (time.perf_counter() - start_time) * 1000.0

    # Ensure result dictionary shape
    if not isinstance(result, dict):
        return {
            "status": "INVALID_RESULT",
            "solution": None,
            "validation_report": None,
            "metrics": {
                "runtime_ms": total_runtime_ms,
                "algorithm": canonical_algo,
                "error": f"Solver returned non-dictionary result: {type(result).__name__}",
            },
        }

    # Ensure metrics dictionary exists
    metrics = result.get("metrics")
    if not isinstance(metrics, dict):
        metrics = {}
        result["metrics"] = metrics
    metrics.setdefault("runtime_ms", total_runtime_ms)
    metrics["algorithm"] = canonical_algo

    status = result.get("status")
    solution = result.get("solution")

    # 6. Independent Validation Safeguard
    if status == "SOLVED":
        if not isinstance(solution, dict) or "bridge_counts" not in solution:
            result["status"] = "INVALID_RESULT"
            result["solution"] = None
            result["validation_report"] = None
            metrics["validation_error"] = "Solver reported SOLVED but solution dictionary is missing or invalid"
            return result

        # Run independent verification
        report = validate_solution(puzzle, solution)
        if report["valid"] is True:
            result["status"] = "SOLVED"
            result["validation_report"] = report
        else:
            # Override status: Algorithm claimed success, but independent validator found violations!
            result["status"] = "INVALID_RESULT"
            result["validation_report"] = report
            metrics["validation_error"] = "Solution claimed by solver failed independent validation safeguard"

    return result
