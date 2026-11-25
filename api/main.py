"""FastAPI layer. Run:  uvicorn api.main:app --reload   (from the repo root)

/validate and /solve are fully implemented via core.algorithm_runner.
Contract is described in docs/SYSTEM_ARCHITECTURE.md.
"""
from __future__ import annotations

from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from core.algorithm_runner import list_supported_algorithms, run_algorithm
from core.candidate_generator import generate_candidate_edges
from core.solution_validator import validate_solution

app = FastAPI(title="Hashiwokakero Solver API", version="1.0.0")

# Allow all origins for development (frontend running on a different port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class IslandModel(BaseModel):
    id: str
    row: int = Field(ge=0)
    col: int = Field(ge=0)
    required_bridges: int = Field(ge=1, le=8)


class PuzzleModel(BaseModel):
    rows: int = Field(ge=1)
    cols: int = Field(ge=1)
    islands: List[IslandModel]


class SolveRequest(BaseModel):
    puzzle: PuzzleModel
    algorithm: str
    config: Optional[dict] = None


class ValidateRequest(BaseModel):
    puzzle: PuzzleModel
    solution: dict  # {"bridge_counts": {edge_id: 0|1|2}}


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    """Health check — returns 200 OK with status information."""
    return {"status": "ok"}


@app.get("/algorithms")
def algorithms() -> List[str]:
    """List the available solving algorithms."""
    return list_supported_algorithms()


@app.post("/candidate-bridges")
def candidate_bridges(puzzle: PuzzleModel) -> dict:
    """Return all candidate bridges for the given puzzle.

    Used by the frontend to know which edges exist before the solver runs.
    """
    islands = [isl.model_dump() for isl in puzzle.islands]
    edges = generate_candidate_edges(islands)
    return {"candidate_bridges": edges}


@app.post("/validate")
def validate(req: ValidateRequest) -> dict:
    """Validate a proposed solution against the puzzle rules.

    Returns a ValidationReport with:
      valid, degree_violations, crossings, connected_components, invalid_values
    """
    try:
        puzzle = req.puzzle.model_dump()
        return validate_solution(puzzle, req.solution)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/solve")
def solve(req: SolveRequest) -> dict:
    """Solve the puzzle using the requested algorithm via the unified Algorithm Runner.

    Returns the standard SolverResult:
      { status, solution, validation_report, metrics }
    """
    try:
        puzzle = req.puzzle.model_dump()
        result = run_algorithm(puzzle, req.algorithm, config=req.config)
        # INVALID_INPUT means the runner rejected the request (bad algo name or puzzle)
        if result.get("status") == "INVALID_INPUT":
            raise HTTPException(status_code=400, detail=result["metrics"].get("error", "Invalid input"))
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
