"""FastAPI layer. Run:  uvicorn api.main:app --reload   (from the repo root)

/validate and /solve answer 501 until the underlying modules are implemented.
Contract is described in docs/SYSTEM_ARCHITECTURE.md.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from algorithms.backtracking import solve_backtracking
from algorithms.genetic import solve_genetic
from algorithms.memetic import solve_memetic
from core.solution_validator import validate_solution

ALGORITHMS = {
    "backtracking": solve_backtracking,
    "genetic": solve_genetic,
    "memetic": solve_memetic,
}

app = FastAPI(title="Hashiwokakero Solver API")


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
    solution: Dict[str, Dict[str, int]]  # {"bridge_counts": {...}}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/algorithms")
def algorithms() -> List[str]:
    return list(ALGORITHMS)


@app.post("/validate")
def validate(req: ValidateRequest) -> dict:
    try:
        return validate_solution(req.puzzle.model_dump(), req.solution)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))


@app.post("/solve")
def solve(req: SolveRequest) -> dict:
    solver = ALGORITHMS.get(req.algorithm)
    if solver is None:
        raise HTTPException(status_code=400, detail=f"Unknown algorithm: {req.algorithm}")
    try:
        if req.algorithm == "backtracking":
            return solver(req.puzzle.model_dump())
        return solver(req.puzzle.model_dump(), params=req.config)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail=str(exc))
