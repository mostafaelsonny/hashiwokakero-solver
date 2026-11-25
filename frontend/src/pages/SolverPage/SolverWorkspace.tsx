import React from "react";
import { JsonPreview } from "../../components/JsonPreview";
import { PuzzleGrid } from "../../components/PuzzleGrid/PuzzleGrid";
import { SolverPanel } from "../../components/SolverPanel";
import { BackendDebugPanel } from "../../devtools/BackendDebugPanel";
import type { Algorithm, CandidateBridge, Puzzle, SolveResult } from "../../types";

interface SolverWorkspaceProps {
  puzzle: Puzzle;
  algorithm: Algorithm;
  candidateBridges: CandidateBridge[];
  solveResult: SolveResult | null;
  isSolving: boolean;
  onCellClick: (row: number, col: number) => void;
  onIslandRightClick: (id: string) => void;
  onIslandCycleValue: (id: string) => void;
  onSolve: () => void;
}

export function SolverWorkspace({
  puzzle,
  algorithm,
  candidateBridges,
  solveResult,
  isSolving,
  onCellClick,
  onIslandRightClick,
  onIslandCycleValue,
  onSolve,
}: SolverWorkspaceProps) {
  const { rows, cols, islands } = puzzle;

  return (
    <main className="app-main">
      <PuzzleGrid
        rows={rows}
        cols={cols}
        islands={islands}
        candidateBridges={candidateBridges}
        solvedBridgeCounts={solveResult?.solution?.bridge_counts ?? null}
        onCellClick={onCellClick}
        onIslandRightClick={onIslandRightClick}
        onIslandCycleValue={onIslandCycleValue}
      />

      <p className="hint-text">
        {islands.length === 0
          ? "👉 Click any square on the board or load a preset (P1 / P2) to begin."
          : `✓ ${islands.length} island${islands.length !== 1 ? "s" : ""} placed. Click to cycle bridge counts (1-8), right-click to remove.`}
      </p>

      <SolverPanel
        algorithm={algorithm}
        isSolving={isSolving}
        hasIslands={islands.length > 0}
        solveResult={solveResult}
        onSolve={onSolve}
      />

      {import.meta.env.DEV && <BackendDebugPanel puzzle={puzzle} />}

      <JsonPreview puzzle={puzzle} />
    </main>
  );
}
