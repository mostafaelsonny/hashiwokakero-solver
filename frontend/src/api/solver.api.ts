import type { Algorithm, CandidateBridge, Puzzle, Solution, SolveResult, ValidationReport } from "../types";

async function post<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`/api${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`${path} failed (${response.status}): ${errorText}`);
  }
  return (await response.json()) as T;
}

export const getCandidateBridges = (puzzle: Puzzle) =>
  post<{ candidate_bridges: CandidateBridge[] }>("/candidate-bridges", puzzle);

export const solve = (puzzle: Puzzle, algorithm: Algorithm, config?: Record<string, unknown>) =>
  post<SolveResult>("/solve", { puzzle, algorithm, config });

export const validate = (puzzle: Puzzle, solution: Solution) =>
  post<ValidationReport>("/validate", { puzzle, solution });
