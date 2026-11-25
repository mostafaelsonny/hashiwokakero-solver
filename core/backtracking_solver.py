from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

from core.backtracking_state import BacktrackingState
from core.crossing_detector import get_crossing_pairs
from core.models import CandidateBridge, Puzzle, Solution
from core.solution_validator import validate_solution


DEFAULT_MAX_STATES = 100_000
DEFAULT_TIMEOUT_MS = 10_000
DEFAULT_VALUE_ORDER = [1, 2, 0]


def _read_config(
    config: Optional[Dict[str, Any]],
) -> Tuple[int, int, List[int]]:
    """اقرأ إعدادات البحث وتحقق من صلاحيتها."""
    if config is None:
        config = {}

    if not isinstance(config, dict):
        raise ValueError("config must be a dictionary or None")

    max_states = config.get("max_states", DEFAULT_MAX_STATES)
    timeout_ms = config.get("timeout_ms", DEFAULT_TIMEOUT_MS)
    value_order = config.get("value_order", DEFAULT_VALUE_ORDER)

    if type(max_states) is not int or max_states < 1:
        raise ValueError(
            "max_states must be an integer greater than or equal to 1"
        )

    if type(timeout_ms) is not int or timeout_ms < 100:
        raise ValueError(
            "timeout_ms must be an integer greater than or equal to 100"
        )

    if (
        not isinstance(value_order, list)
        or any(type(value) is not int for value in value_order)
        or sorted(value_order) != [0, 1, 2]
    ):
        raise ValueError("value_order must be a permutation of [0, 1, 2]")

    # ننسخ القائمة حتى لا نغير config الذي أرسله المستدعي.
    return max_states, timeout_ms, value_order.copy()


def solve_backtracking(
    puzzle: Puzzle,
    candidate_bridges: List[CandidateBridge],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """حل اللغز باستخدام بحث DFS تكراري مع pruning وrollback.

    يجب أن تكون candidate_bridges هي القائمة canonical E1..En الخاصة باللغز.
    الدالة تستخدم القائمة المستلمة كما هي ولا تعيد ترتيبها أو تعديلها.
    """
    started_at = time.perf_counter()

    metrics: Dict[str, Any] = {
        "runtime_ms": 0.0,
        "explored_states": 0,
        "backtracks": 0,
        "pruned_degree_upper": 0,
        "pruned_degree_lower": 0,
        "pruned_crossing": 0,
    }

    def finish(
        status: str,
        solution: Optional[Solution] = None,
        validation_report: Optional[dict] = None,
    ) -> Dict[str, Any]:
        """كوّن النتيجة الموحدة وحدّث زمن التنفيذ."""
        metrics["runtime_ms"] = (
            time.perf_counter() - started_at
        ) * 1000.0

        return {
            "status": status,
            "solution": solution,
            "validation_report": validation_report,
            "metrics": metrics.copy(),
        }

    try:
        max_states, timeout_ms, value_order = _read_config(config)

        # تحقق أساسي من IDs ونقاط نهاية candidates، من غير إعادة ترتيبها.
        island_ids = [island["id"] for island in puzzle["islands"]]
        if len(set(island_ids)) != len(island_ids):
            raise ValueError("Puzzle contains duplicate island IDs")

        island_id_set = set(island_ids)
        candidate_ids = [candidate["id"] for candidate in candidate_bridges]

        if len(set(candidate_ids)) != len(candidate_ids):
            raise ValueError("Candidate list contains duplicate IDs")

        for index, candidate in enumerate(candidate_bridges, start=1):
            if candidate["id"] != f"E{index}":
                raise ValueError(
                    "Candidate IDs must follow the supplied E1..En order"
                )

            if candidate["from"] not in island_id_set:
                raise ValueError(
                    f"{candidate['id']} references an unknown from-island"
                )

            if candidate["to"] not in island_id_set:
                raise ValueError(
                    f"{candidate['id']} references an unknown to-island"
                )

            if candidate["from"] == candidate["to"]:
                raise ValueError(
                    f"{candidate['id']} has identical endpoints"
                )

        state = BacktrackingState(
            puzzle["islands"],
            candidate_bridges,
        )

        # 1. فحص مبدئي سريع: هل يمتلك اللغز سعة كافية لكل الجزر من الأساس؟
        # إذا كانت هناك جزيرة معزولة أو سعتها المتاحة أقل من المطلوب ننهي فوراً بـ UNSATISFIABLE.
        if not state.is_feasible():
            return finish("UNSATISFIABLE")

        deadline = started_at + timeout_ms / 1000.0

        # تجهيز أطراف كل candidate مسبقاً للوصول السريع بـ O(1)
        endpoints_by_index = [
            (candidate["from"], candidate["to"])
            for candidate in candidate_bridges
        ]

        # جهّز فهرس تقاطعات حسب مواقع الـcandidates في القائمة الأصلية.
        index_by_id = {
            candidate["id"]: index
            for index, candidate in enumerate(candidate_bridges)
        }

        crossing_edges_by_index: List[List[int]] = [
            [] for _ in candidate_bridges
        ]

        for first_id, second_id in get_crossing_pairs(
            puzzle["islands"],
            candidate_bridges,
        ):
            first_idx = index_by_id[first_id]
            second_idx = index_by_id[second_id]

            crossing_edges_by_index[first_idx].append(second_idx)
            crossing_edges_by_index[second_idx].append(first_idx)

        found_solution: Optional[Solution] = None
        found_report: Optional[dict] = None

        def search(candidate_idx: int) -> str:
            """ترجع solved أو exhausted أو limit."""
            nonlocal found_solution, found_report

            # لا تبدأ حالة جديدة لو استُهلك الحد أو انتهى الوقت.
            if metrics["explored_states"] >= max_states:
                return "limit"

            if time.perf_counter() >= deadline:
                return "limit"

            metrics["explored_states"] += 1

            # كل candidates أُسندت. مرر الحل للـvalidator كفحص نهائي.
            if candidate_idx == len(candidate_bridges):
                solution: Solution = {
                    "bridge_counts": {
                        candidate["id"]: state.assignments[index]
                        for index, candidate in enumerate(candidate_bridges)
                    }
                }

                report = validate_solution(puzzle, solution)

                if report["valid"] is True:
                    found_solution = solution
                    found_report = report
                    return "solved"

                # قد تكون الدرجات صحيحة لكن الشبكة مفصولة؛ أكمل البحث.
                return "exhausted"

            first, second = endpoints_by_index[candidate_idx]

            for count in value_order:
                state.assign(candidate_idx, count)

                try:
                    # 1. Upper bound: فحص O(1) لطرفي الجسر الحالي فقط
                    # (أي جزيرة أخرى لم تتغير درجتها فمستحيل أن تتجاوز المطلوب)
                    if (
                        state.current_degree[first] > state.required_bridges[first]
                        or state.current_degree[second] > state.required_bridges[second]
                    ):
                        metrics["pruned_degree_upper"] += 1
                        branch_result = "exhausted"

                    # 2. Lower bound: فحص O(1) لسعة طرفي الجسر الحالي فقط
                    # (بما أن الحالة كانت feasible قبل الإسناد، فالطرفان هما فقط من نقصت سعتهما)
                    elif (
                        state.current_degree[first] + state.remaining_capacity[first]
                        < state.required_bridges[first]
                        or state.current_degree[second] + state.remaining_capacity[second]
                        < state.required_bridges[second]
                    ):
                        metrics["pruned_degree_lower"] += 1
                        branch_result = "exhausted"

                    # 3. Crossing: افحص فقط عند اختيار جسر موجب،
                    # وعلى الجسور التي تتقاطع مع candidate الحالي.
                    elif count > 0 and any(
                        state.assignments[crossing_idx] is not None
                        and state.assignments[crossing_idx] > 0
                        for crossing_idx
                        in crossing_edges_by_index[candidate_idx]
                    ):
                        metrics["pruned_crossing"] += 1
                        branch_result = "exhausted"

                    else:
                        branch_result = search(candidate_idx + 1)

                finally:
                    # كل فرع يرجع الحالة كما كانت قبل تجربة القيمة.
                    state.undo(candidate_idx, count)

                if branch_result == "solved":
                    return "solved"

                if branch_result == "limit":
                    return "limit"

                metrics["backtracks"] += 1

            return "exhausted"

        outcome = search(0)

        if outcome == "solved":
            return finish(
                "SOLVED",
                found_solution,
                found_report,
            )

        if outcome == "limit":
            return finish("LIMIT_REACHED")

        return finish("UNSATISFIABLE")

    except Exception as error:
        # عقد الواجهة يطلب إرجاع SolverResult بدل ترك الاستثناء يخرج للمشغّل.
        metrics["error"] = str(error)
        return finish("INVALID_INPUT")