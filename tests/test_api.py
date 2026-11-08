"""API smoke tests (always run). /validate and /solve return 501 until modules exist."""
from fastapi.testclient import TestClient

from api.main import app
from tests.helpers import P1_PUZZLE

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_algorithms_listed():
    assert client.get("/algorithms").json() == ["backtracking", "genetic", "memetic"]


def test_unknown_algorithm_is_400():
    response = client.post("/solve", json={"puzzle": P1_PUZZLE, "algorithm": "nope"})
    assert response.status_code == 400


def test_solve_not_implemented_yet_is_501():
    response = client.post("/solve", json={"puzzle": P1_PUZZLE, "algorithm": "backtracking"})
    assert response.status_code in (200, 501)
