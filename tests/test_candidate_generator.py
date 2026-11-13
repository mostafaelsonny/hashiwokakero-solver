
from core.candidate_generator import generate_candidate_edges
from tests.helpers import P1_ISLANDS, P2_ISLANDS


def test_two_islands_same_row():
    islands = [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
        {"id": "B", "row": 0, "col": 3, "required_bridges": 2},
    ]

    expected = [
        {
            "id": "E1",
            "from": "A",
            "to": "B",
            "orientation": "horizontal",
        }
    ]

    assert generate_candidate_edges(islands) == expected


def test_two_islands_same_column():
    islands = [
        {"id": "A", "row": 0, "col": 2, "required_bridges": 2},
        {"id": "B", "row": 3, "col": 2, "required_bridges": 2},
    ]

    expected = [
        {
            "id": "E1",
            "from": "A",
            "to": "B",
            "orientation": "vertical",
        }
    ]

    assert generate_candidate_edges(islands) == expected


def test_three_islands_in_same_row_connect_nearest_only():
    islands = [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
        {"id": "B", "row": 0, "col": 2, "required_bridges": 2},
        {"id": "C", "row": 0, "col": 4, "required_bridges": 2},
    ]

    expected = [
        {
            "id": "E1",
            "from": "A",
            "to": "B",
            "orientation": "horizontal",
        },
        {
            "id": "E2",
            "from": "B",
            "to": "C",
            "orientation": "horizontal",
        },
    ]

    assert generate_candidate_edges(islands) == expected


def test_diagonal_islands_do_not_connect():
    islands = [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
        {"id": "B", "row": 2, "col": 2, "required_bridges": 2},
    ]

    assert generate_candidate_edges(islands) == []


def test_single_island_returns_empty_list():
    islands = [
        {"id": "A", "row": 0, "col": 0, "required_bridges": 2},
    ]

    assert generate_candidate_edges(islands) == []


def test_p1_expected_edges_and_order():
    expected = [
        {
            "id": "E1",
            "from": "A",
            "to": "B",
            "orientation": "horizontal",
        },
        {
            "id": "E2",
            "from": "A",
            "to": "C",
            "orientation": "vertical",
        },
        {
            "id": "E3",
            "from": "B",
            "to": "D",
            "orientation": "vertical",
        },
        {
            "id": "E4",
            "from": "C",
            "to": "D",
            "orientation": "horizontal",
        },
    ]

    assert generate_candidate_edges(P1_ISLANDS) == expected


def test_p2_expected_edges_and_order():
    expected = [
        {
            "id": "E1",
            "from": "C",
            "to": "D",
            "orientation": "vertical",
        },
        {
            "id": "E2",
            "from": "A",
            "to": "B",
            "orientation": "horizontal",
        },
    ]

    assert generate_candidate_edges(P2_ISLANDS) == expected


def test_input_order_does_not_change_result():
    original_result = generate_candidate_edges(P1_ISLANDS)

    shuffled_islands = [
        P1_ISLANDS[3],
        P1_ISLANDS[1],
        P1_ISLANDS[0],
        P1_ISLANDS[2],
    ]

    shuffled_result = generate_candidate_edges(shuffled_islands)

    assert shuffled_result == original_result
