"""S1-07 - Final Solution Validator.  Owner: Ebrahim.  Reviewers: Mostafa + Monzer.

THE single judge of correctness. It must REUSE the functions from S1-03/04/05/06
(no duplicated rule logic). No algorithm may report "Solution Found" unless
validate_solution(...)["valid"] is True.
"""
from __future__ import annotations

from core.models import Puzzle, Solution, ValidationReport


def validate_solution(puzzle: Puzzle, solution: Solution) -> ValidationReport:
    """Return the full report (all problems at once, never stop at the first one).

    Steps: (1) values: each in {0,1,2}, edge ids must exist (missing id = 0)
           (2) degree check, mode="final"   (3) crossings   (4) connectivity (exactly 1 component)
    valid is True iff: no invalid values, no degree violations, no crossings, components == 1.
    """
    raise NotImplementedError("S1-07 not implemented yet (owner: Ebrahim)")
