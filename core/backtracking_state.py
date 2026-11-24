from __future__ import annotations

from typing import Dict, List, Optional, Sequence

from core.models import CandidateBridge, Island, VALID_BRIDGE_VALUES


class BacktrackingState:
    """حالة البحث الداخلية مع الحفاظ على ترتيب الـ candidates كما استلمناه."""

    def __init__(
        self,
        islands: Sequence[Island],
        candidates: Sequence[CandidateBridge],
    ):
        # None تعني أن الـ candidate لم يُحسم بعد؛ أما 0 فهو إسناد صريح.
        self.assignments: List[Optional[int]] = [None] * len(candidates)

        self.current_degree: Dict[str, int] = {
            island["id"]: 0 for island in islands
        }
        self.remaining_capacity: Dict[str, int] = {
            island["id"]: 0 for island in islands
        }
        self.required_bridges: Dict[str, int] = {
            island["id"]: island["required_bridges"] for island in islands
        }

        self._endpoints: List[tuple[str, str]] = []

        for candidate in candidates:
            first = candidate["from"]
            second = candidate["to"]

            if first not in self.remaining_capacity or second not in self.remaining_capacity:
                raise ValueError(
                    f"candidate {candidate['id']} references an unknown island"
                )

            self._endpoints.append((first, second))

            # كل candidate غير محسوم يمكن أن يضيف جسرين لكل طرف.
            self.remaining_capacity[first] += 2
            self.remaining_capacity[second] += 2

    def assign(self, candidate_idx: int, count: int) -> None:
        """يسند 0 أو 1 أو 2 ويحدّث درجتي الجزيرتين وسعتيهما."""
        self._validate_index(candidate_idx)

        if type(count) is not int or count not in VALID_BRIDGE_VALUES:
            raise ValueError("count must be an integer in {0, 1, 2}")

        if self.assignments[candidate_idx] is not None:
            raise ValueError(f"candidate index {candidate_idx} is already assigned")

        first, second = self._endpoints[candidate_idx]
        self.assignments[candidate_idx] = count

        for island_id in (first, second):
            self.current_degree[island_id] += count
            self.remaining_capacity[island_id] -= 2

    def undo(self, candidate_idx: int, count: int) -> None:
        """يلغي الإسناد المطابق ويعيد الحالة السابقة."""
        self._validate_index(candidate_idx)

        if type(count) is not int or count not in VALID_BRIDGE_VALUES:
            raise ValueError("count must be an integer in {0, 1, 2}")

        if self.assignments[candidate_idx] != count:
            raise ValueError("undo count must match the candidate's current assignment")

        first, second = self._endpoints[candidate_idx]
        self.assignments[candidate_idx] = None

        for island_id in (first, second):
            self.current_degree[island_id] -= count
            self.remaining_capacity[island_id] += 2

    def is_feasible(self) -> bool:
        """يتحقق أن السعة المتبقية تسمح لكل جزيرة بإكمال درجتها المطلوبة."""
        return all(
            self.current_degree[island_id] + self.remaining_capacity[island_id]
            >= required
            for island_id, required in self.required_bridges.items()
        )

    def _validate_index(self, candidate_idx: int) -> None:
        if (
            type(candidate_idx) is not int
            or not 0 <= candidate_idx < len(self.assignments)
        ):
            raise IndexError("candidate_idx is outside the candidate list")