"""S1-12 - Integration Tests. Owner: Mostafa. Reviewer: Ebrahim + Monzer.

End-to-end tests that go through the full stack:
  puzzle → API → core modules → validated result
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from tests.helpers import P1_PUZZLE, P2_PUZZLE, p1, p2

client = TestClient(app)


# ---------------------------------------------------------------------------
# Health & Discovery
# ---------------------------------------------------------------------------

def test_health_returns_ok():
    """GET /health should return 200 with status=ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"


def test_algorithms_endpoint_lists_three():
    """GET /algorithms should list all three algorithms."""
    response = client.get("/algorithms")
    assert response.status_code == 200
    algorithms = response.json()
    assert set(algorithms) == {"backtracking", "genetic", "memetic"}


# ---------------------------------------------------------------------------
# /candidate-bridges
# ---------------------------------------------------------------------------

def test_candidate_bridges_p1():
    """POST /candidate-bridges for P1 should return 4 edges."""
    response = client.post("/candidate-bridges", json=P1_PUZZLE)
    assert response.status_code == 200
    data = response.json()
    assert "candidate_bridges" in data
    edges = data["candidate_bridges"]
    assert len(edges) == 4
    # Every edge must have the correct fields
    for e in edges:
        assert "id" in e
        assert "from" in e
        assert "to" in e
        assert "orientation" in e
        assert e["orientation"] in ("horizontal", "vertical")


def test_candidate_bridges_p2():
    """POST /candidate-bridges for P2 should return 2 crossing edges."""
    response = client.post("/candidate-bridges", json=P2_PUZZLE)
    assert response.status_code == 200
    edges = response.json()["candidate_bridges"]
    assert len(edges) == 2
    orientations = {e["orientation"] for e in edges}
    assert "horizontal" in orientations
    assert "vertical" in orientations


# ---------------------------------------------------------------------------
# /validate
# ---------------------------------------------------------------------------

def test_validate_known_valid_solution():
    """POST /validate with the perfect P1 solution should return valid=True."""
    solution = p1([1, 1, 1, 1])
    response = client.post("/validate", json={"puzzle": P1_PUZZLE, "solution": solution})
    assert response.status_code == 200
    report = response.json()
    assert report["valid"] is True
    assert report["degree_violations"] == []
    assert report["crossings"] == []
    assert report["connected_components"] == 1
    assert report["invalid_values"] == []


def test_validate_degree_violation_reported():
    """POST /validate with a wrong solution should report degree violations."""
    solution = p1([0, 0, 0, 0])  # all zeros → all islands unsatisfied
    response = client.post("/validate", json={"puzzle": P1_PUZZLE, "solution": solution})
    assert response.status_code == 200
    report = response.json()
    assert report["valid"] is False
    assert len(report["degree_violations"]) == 4  # all 4 islands violated


def test_validate_crossing_reported():
    """POST /validate for P2 with both bridges should report a crossing."""
    solution = p2([1, 1])
    response = client.post("/validate", json={"puzzle": P2_PUZZLE, "solution": solution})
    assert response.status_code == 200
    report = response.json()
    assert report["valid"] is False
    assert len(report["crossings"]) == 1


def test_validate_disconnected_graph_reported():
    """POST /validate for a split graph should report components > 1."""
    solution = p1([2, 0, 0, 2])  # A-B connected, C-D connected, split
    response = client.post("/validate", json={"puzzle": P1_PUZZLE, "solution": solution})
    assert response.status_code == 200
    report = response.json()
    assert report["valid"] is False
    assert report["connected_components"] == 2
    assert report["degree_violations"] == []


def test_validate_invalid_bridge_value_reported():
    """POST /validate with bridge count=3 should report it in invalid_values."""
    solution = {"bridge_counts": {"E1": 3, "E2": 1, "E3": 1, "E4": 1}}
    response = client.post("/validate", json={"puzzle": P1_PUZZLE, "solution": solution})
    assert response.status_code == 200
    report = response.json()
    assert report["valid"] is False
    assert any(item["edge"] == "E1" for item in report["invalid_values"])


def test_solve_unknown_algorithm_is_400():
    """POST /solve with unknown algorithm must return 400."""
    response = client.post("/solve", json={"puzzle": P1_PUZZLE, "algorithm": "quantum"})
    assert response.status_code == 400
