import random

import pytest

from algorithms.ga.chromosome import (
    chromosome_to_solution,
    initialize_population,
    solution_to_chromosome,
)
from algorithms.ga.fitness import build_conflict_pairs, evaluate_fitness

# ---- Canonical P1 (docs/DATA_MODEL.md section 9) ---------------------------------
P1 = {
    "rows": 3,
    "cols": 3,
    "islands": [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
        {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
        {"id": "C", "row": 2, "col": 0, "required_bridges": 2},
        {"id": "D", "row": 2, "col": 2, "required_bridges": 2},
    ],
}
P1_CANDIDATES = [
    {"id": "E1", "from": "A", "to": "B", "orientation": "horizontal"},
    {"id": "E2", "from": "A", "to": "C", "orientation": "vertical"},
    {"id": "E3", "from": "B", "to": "D", "orientation": "vertical"},
    {"id": "E4", "from": "C", "to": "D", "orientation": "horizontal"},
]

# ---- Plus-shaped puzzle: E1 (vertical) crosses E2 (horizontal) -----------------
PLUS = {
    "rows": 3,
    "cols": 3,
    "islands": [
        {"id": "T", "row": 0, "col": 1, "required_bridges": 1},
        {"id": "L", "row": 1, "col": 0, "required_bridges": 1},
        {"id": "R", "row": 1, "col": 2, "required_bridges": 1},
        {"id": "B", "row": 2, "col": 1, "required_bridges": 1},
    ],
}
PLUS_CANDIDATES = [
    {"id": "E1", "from": "T", "to": "B", "orientation": "vertical"},
    {"id": "E2", "from": "L", "to": "R", "orientation": "horizontal"},
]


# ---- Conversion ------------------------------------------------------------------
def test_chromosome_to_solution_p1():
    assert chromosome_to_solution([1, 1, 1, 1], P1_CANDIDATES) == {
        "bridge_counts": {"E1": 1, "E2": 1, "E3": 1, "E4": 1}
    }


@pytest.mark.parametrize(
    "chromosome", [[1, 1, 1, 1], [2, 0, 0, 2], [0, 0, 0, 0], [2, 2, 2, 2], [0, 1, 2, 1]]
)
def test_round_trip_is_lossless(chromosome):
    solution = chromosome_to_solution(chromosome, P1_CANDIDATES)
    assert solution_to_chromosome(solution, P1_CANDIDATES) == chromosome


def test_missing_known_ids_are_zero():
    assert solution_to_chromosome({"bridge_counts": {"E3": 2}}, P1_CANDIDATES) == [0, 0, 2, 0]
    assert solution_to_chromosome({"bridge_counts": {}}, P1_CANDIDATES) == [0, 0, 0, 0]


def test_explicit_zero_entries_are_accepted():
    solution = {"bridge_counts": {"E1": 1, "E2": 0, "E3": 2, "E4": 1}}
    assert solution_to_chromosome(solution, P1_CANDIDATES) == [1, 0, 2, 1]


@pytest.mark.parametrize(
    "bad",
    [[1, 1, 1, 3], [1, 1, 1, -1], [1, True, 1, 1], [1, 1.0, 1, 1], [1, "1", 1, 1], [1, None, 1, 1]],
)
def test_invalid_gene_values_rejected(bad):
    with pytest.raises(ValueError, match="chromosome_gene_must_be_integer_0_1_or_2"):
        chromosome_to_solution(bad, P1_CANDIDATES)


@pytest.mark.parametrize("bad", [[1, 1, 1], [1, 1, 1, 1, 1], []])
def test_length_mismatch_rejected(bad):
    with pytest.raises(ValueError, match="chromosome_length_mismatch"):
        chromosome_to_solution(bad, P1_CANDIDATES)


def test_chromosome_must_be_a_list():
    with pytest.raises(ValueError):
        chromosome_to_solution((1, 1, 1, 1), P1_CANDIDATES)


def test_unknown_bridge_id_rejected():
    with pytest.raises(ValueError, match="unknown_candidate_bridge_id"):
        solution_to_chromosome({"bridge_counts": {"E99": 1}}, P1_CANDIDATES)


@pytest.mark.parametrize("bad_count", [3, -1, True, 1.0, "2"])
def test_invalid_bridge_count_rejected(bad_count):
    with pytest.raises(ValueError, match="bridge_count_must_be_integer_0_1_or_2"):
        solution_to_chromosome({"bridge_counts": {"E1": bad_count}}, P1_CANDIDATES)


def test_solution_without_bridge_counts_rejected():
    with pytest.raises(ValueError):
        solution_to_chromosome({}, P1_CANDIDATES)


def test_conversion_does_not_mutate_candidates():
    snapshot = [dict(b) for b in P1_CANDIDATES]
    chromosome_to_solution([1, 0, 2, 1], P1_CANDIDATES)
    assert P1_CANDIDATES == snapshot


# ---- Population ------------------------------------------------------------------
def test_population_shape_and_domain():
    population = initialize_population(25, 4, seed=7)
    assert len(population) == 25
    for chromosome in population:
        assert len(chromosome) == 4
        assert all(type(g) is int and g in (0, 1, 2) for g in chromosome)
        chromosome_to_solution(chromosome, P1_CANDIDATES)  # must be convertible


def test_population_same_seed_is_reproducible():
    assert initialize_population(10, 6, seed=42) == initialize_population(10, 6, seed=42)
    assert initialize_population(10, 6, seed=1) != initialize_population(10, 6, seed=2)


def test_population_does_not_touch_global_random_state():
    random.seed(123)
    expected = random.random()
    random.seed(123)
    initialize_population(5, 5, seed=99)
    assert random.random() == expected


@pytest.mark.parametrize("pop,length", [(-1, 4), (4, -1), (True, 4), (4, 2.0)])
def test_population_bad_arguments(pop, length):
    with pytest.raises(ValueError):
        initialize_population(pop, length)


def test_population_empty_cases():
    assert initialize_population(0, 4) == []
    assert initialize_population(3, 0) == [[], [], []]


# ---- Fitness: manual P1 cases from the task card -----------------------------------
@pytest.mark.parametrize(
    "chromosome,expected",
    [
        ([1, 1, 1, 1], (0, 0, 0)),
        ([1, 0, 1, 1], (2, 0, 0)),
        ([2, 0, 0, 2], (0, 0, 1)),
        ([2, 2, 0, 0], (4, 0, 1)),
    ],
)
def test_p1_fitness(chromosome, expected):
    assert evaluate_fitness(chromosome, P1, P1_CANDIDATES) == expected


def test_p1_has_no_conflicts():
    assert build_conflict_pairs(P1, P1_CANDIDATES) == []


def test_fitness_lexicographic_ordering():
    best = evaluate_fitness([1, 1, 1, 1], P1, P1_CANDIDATES)
    worse = evaluate_fitness([2, 0, 0, 2], P1, P1_CANDIDATES)
    assert best < worse


# ---- Fitness: crossings --------------------------------------------------------------
def test_conflict_pairs_detects_crossing():
    assert build_conflict_pairs(PLUS, PLUS_CANDIDATES) == [(0, 1)]


def test_crossing_counted_only_when_both_selected():
    assert evaluate_fitness([1, 1], PLUS, PLUS_CANDIDATES) == (0, 1, 1)
    assert evaluate_fitness([1, 0], PLUS, PLUS_CANDIDATES)[1] == 0
    assert evaluate_fitness([0, 1], PLUS, PLUS_CANDIDATES)[1] == 0


def test_double_bridges_do_not_double_count_crossing():
    assert evaluate_fitness([2, 2], PLUS, PLUS_CANDIDATES)[1] == 1


def test_touching_at_endpoint_is_not_a_crossing():
    # L-shape: vertical A-C and horizontal A-B share island A (no crossing).
    assert build_conflict_pairs(P1, P1_CANDIDATES) == []


def test_precomputed_conflicts_give_identical_result():
    conflicts = build_conflict_pairs(PLUS, PLUS_CANDIDATES)
    for chromosome in ([0, 0], [1, 0], [0, 2], [1, 1], [2, 2]):
        assert evaluate_fitness(chromosome, PLUS, PLUS_CANDIDATES) == evaluate_fitness(
            chromosome, PLUS, PLUS_CANDIDATES, conflicts=conflicts
        )


# ---- Fitness: connectivity ---------------------------------------------------------
def test_isolated_island_counts_as_component():
    # Only E1 selected: components {A,B}, {C}, {D} -> penalty 2.
    assert evaluate_fitness([1, 0, 0, 0], P1, P1_CANDIDATES)[2] == 2


def test_empty_chromosome_all_islands_isolated():
    assert evaluate_fitness([0, 0, 0, 0], P1, P1_CANDIDATES) == (8, 0, 3)


def test_double_bridge_is_single_adjacency_for_connectivity():
    assert evaluate_fitness([2, 0, 0, 0], P1, P1_CANDIDATES)[2] == 2


# ---- Fitness: error handling --------------------------------------------------------
def test_fitness_rejects_invalid_chromosome():
    with pytest.raises(ValueError):
        evaluate_fitness([1, True, 1, 1], P1, P1_CANDIDATES)
    with pytest.raises(ValueError):
        evaluate_fitness([1, 1, 1], P1, P1_CANDIDATES)


def test_fitness_rejects_unknown_island_reference():
    bad = [{"id": "E1", "from": "A", "to": "Z", "orientation": "horizontal"}]
    with pytest.raises(ValueError, match="unknown_island_id"):
        evaluate_fitness([1], P1, bad)
    with pytest.raises(ValueError, match="unknown_island_id"):
        build_conflict_pairs(P1, bad)


def test_fitness_returns_plain_int_tuple():
    result = evaluate_fitness([1, 1, 1, 1], P1, P1_CANDIDATES)
    assert isinstance(result, tuple) and len(result) == 3
    assert all(type(x) is int for x in result)