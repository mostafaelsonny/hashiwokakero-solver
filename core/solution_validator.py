"""S1-07 - Final Solution Validator.  Owner: Ebrahim.  Reviewers: Mostafa + Monzer.

THE single judge of correctness. It must REUSE the functions from S1-03/04/05/06
(no duplicated rule logic). No algorithm may report "Solution Found" unless
validate_solution(...)[\"valid\"] is True.
"""
from __future__ import annotations

from core.candidate_generator import generate_candidate_edges
from core.connectivity_checker import find_connected_components
from core.crossing_detector import detect_crossings
from core.degree_validator import check_degrees
from core.models import Puzzle, Solution, ValidationReport


def validate_solution(puzzle: Puzzle, solution: Solution) -> ValidationReport:
    """Return the full report (all problems at once, never stop at the first one).

    Steps: (1) values: each in {0,1,2}, edge ids must exist (missing id = 0)
           (2) degree check, mode="final"   (3) crossings   (4) connectivity (exactly 1 component)
    valid is True iff: no invalid values, no degree violations, no crossings, components == 1.
    """
    islands = puzzle["islands"]
    edges = generate_candidate_edges(islands)
    known_ids = {e["id"] for e in edges}

    # --- Step 1: Validate bridge count values and edge IDs ---
    invalid_values = []
    valid_counts = {}

    for eid, val in solution["bridge_counts"].items():
        if eid not in known_ids:
            # Unknown edge id
            invalid_values.append({"edge": eid, "value": val})
        elif val not in (0, 1, 2):
            # Invalid bridge count value
            invalid_values.append({"edge": eid, "value": val})
        else:
            # Valid: include in clean solution for further checks
            valid_counts[eid] = val

    # Build a clean solution with only valid, known edge ids
    clean_solution: Solution = {"bridge_counts": valid_counts}

    # --- Step 2: Degree violations (final mode: actual must equal required) ---
    degree_violations = check_degrees(islands, edges, clean_solution, "final")

    # --- Step 3: Crossing detection ---
    crossings = detect_crossings(islands, edges, clean_solution)

    # --- Step 4: Connectivity ---
    components = find_connected_components(islands, edges, clean_solution)
    connected_components = len(components)

    # --- Aggregate result ---
    is_valid = (
        len(invalid_values) == 0
        and len(degree_violations) == 0
        and len(crossings) == 0
        and connected_components == 1
    )

    return {
        "valid": is_valid,
        "degree_violations": degree_violations,
        "crossings": crossings,
        "connected_components": connected_components,
        "invalid_values": invalid_values,
    }
