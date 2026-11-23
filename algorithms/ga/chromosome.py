"""GA / MA shared chromosome utilities (S2-06).

Contract (docs/DATA_MODEL.md section 7 and ALGORITHM_INTERFACE.md section 8):
  * A chromosome is a list[int]; gene i <-> candidate_bridges[i] (E_{i+1}).
  * len(chromosome) == len(candidate_bridges).
  * Every gene is a real int in {0, 1, 2} (bool and float are rejected, no coercion).
  * A known candidate ID missing from Solution.bridge_counts means 0.
  * An unknown candidate ID in a Solution is invalid and is never silently ignored.

Error messages start with the machine-readable reason codes of DATA_MODEL 8.5.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:  # type hints only: no runtime dependency on core.models
    from core.models import CandidateBridge, Solution

VALID_COUNTS = (0, 1, 2)


def _is_valid_count(value) -> bool:
    # `type(...) is int` rejects bool and float (True == 1 and 1.0 == 1 in Python).
    return type(value) is int and value in VALID_COUNTS


def validate_chromosome(chromosome, expected_length: int) -> None:
    """Raise ValueError if the chromosome has a wrong type, length or gene value."""
    if not isinstance(chromosome, list):
        raise ValueError(
            f"chromosome must be a list, got {type(chromosome).__name__}"
        )
    if len(chromosome) != expected_length:
        raise ValueError(
            f"chromosome_length_mismatch: chromosome has {len(chromosome)} genes "
            f"but there are {expected_length} candidate bridges"
        )
    for i, gene in enumerate(chromosome):
        if not _is_valid_count(gene):
            raise ValueError(
                f"chromosome_gene_must_be_integer_0_1_or_2: chromosome[{i}] = {gene!r}"
            )


def chromosome_to_solution(
    chromosome: List[int], candidate_bridges: List["CandidateBridge"]
) -> "Solution":
    """Convert a gene array to {"bridge_counts": {"E1": count, ...}}.

    Zero-count bridges are omitted (DATA_MODEL 6.2: producers SHOULD NOT add 0
    entries); consumers treat a missing known ID as 0, so the round trip is lossless.
    """
    validate_chromosome(chromosome, len(candidate_bridges))

    bridge_counts = {}
    for gene, bridge in zip(chromosome, candidate_bridges):
        if gene > 0:
            bridge_counts[bridge["id"]] = gene
    return {"bridge_counts": bridge_counts}


def solution_to_chromosome(
    solution: "Solution", candidate_bridges: List["CandidateBridge"]
) -> List[int]:
    """Convert {"bridge_counts": {...}} back to a gene array (missing ID -> 0)."""
    bridge_counts = solution.get("bridge_counts") if isinstance(solution, dict) else None
    if not isinstance(bridge_counts, dict):
        raise ValueError("solution must be a dict containing a 'bridge_counts' dict")

    known_ids = {bridge["id"] for bridge in candidate_bridges}
    for bridge_id in bridge_counts:
        if bridge_id not in known_ids:
            raise ValueError(
                f"unknown_candidate_bridge_id: solution.bridge_counts.{bridge_id}"
            )

    chromosome: List[int] = []
    for bridge in candidate_bridges:
        count = bridge_counts.get(bridge["id"], 0)
        if not _is_valid_count(count):
            raise ValueError(
                "bridge_count_must_be_integer_0_1_or_2: "
                f"solution.bridge_counts.{bridge['id']} = {count!r}"
            )
        chromosome.append(count)
    return chromosome


def initialize_population(
    pop_size: int, chromosome_len: int, seed: Optional[int] = None
) -> List[List[int]]:
    """Sample pop_size chromosomes, each gene independently from {0, 1, 2}.

    Uses a local random.Random(seed): reproducible, and the global `random`
    state is never touched.
    """
    for name, value in (("pop_size", pop_size), ("chromosome_len", chromosome_len)):
        if type(value) is not int or value < 0:
            raise ValueError(f"{name} must be a non-negative integer, got {value!r}")

    rng = random.Random(seed)
    return [
        [rng.choice(VALID_COUNTS) for _ in range(chromosome_len)]
        for _ in range(pop_size)
    ]