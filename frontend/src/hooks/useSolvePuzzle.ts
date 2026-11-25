import { useCallback, useState } from "react";
import { getCandidateBridges, solve } from "../api/solver.api";
import type { Algorithm, CandidateBridge, Puzzle, SolveResult } from "../types";

export function useSolvePuzzle() {
  const [solveResult, setSolveResult] = useState<SolveResult | null>(null);
  const [candidateBridges, setCandidateBridges] = useState<CandidateBridge[]>([]);
  const [isSolving, setIsSolving] = useState(false);

  const resetSolution = useCallback(() => {
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  const executeSolve = useCallback(async (puzzle: Puzzle, algorithm: Algorithm) => {
    if (puzzle.islands.length === 0) return;
    setIsSolving(true);
    setSolveResult(null);
    setCandidateBridges([]);

    try {
      const bridgesRes = await getCandidateBridges(puzzle);
      setCandidateBridges(bridgesRes.candidate_bridges);

      const result = await solve(puzzle, algorithm);
      setSolveResult(result);
    } catch (err: unknown) {
      setSolveResult({
        status: "INVALID_INPUT",
        solution: null,
        validation_report: null,
        metrics: { error: String(err) },
      });
    } finally {
      setIsSolving(false);
    }
  }, []);

  return {
    solveResult,
    candidateBridges,
    isSolving,
    executeSolve,
    resetSolution,
  };
}
