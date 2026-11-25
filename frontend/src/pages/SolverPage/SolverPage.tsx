import React, { useCallback, useState } from "react";
import { useBackendHealth } from "../../hooks/useBackendHealth";
import { usePuzzleEditor } from "../../hooks/usePuzzleEditor";
import { useSolvePuzzle } from "../../hooks/useSolvePuzzle";
import type { Algorithm, Puzzle } from "../../types";
import { SolverHeader } from "./SolverHeader";
import { SolverSidebar } from "./SolverSidebar";
import { SolverWorkspace } from "./SolverWorkspace";
import "./SolverPage.css";

export function SolverPage() {
  const [algorithm, setAlgorithm] = useState<Algorithm>("backtracking");

  const {
    rows,
    cols,
    islands,
    puzzle,
    addIsland,
    removeIsland,
    cycleIslandValue,
    changeRows,
    changeCols,
    resetPuzzle,
    loadPreset,
  } = usePuzzleEditor();

  const {
    solveResult,
    candidateBridges,
    isSolving,
    executeSolve,
    resetSolution,
  } = useSolvePuzzle();

  const { isConnected, statusText, checkConnection } = useBackendHealth();

  // Coordinate between puzzle-editor and solver so neither depends on the other
  const handleCellClick = useCallback(
    (row: number, col: number) => {
      addIsland(row, col);
      resetSolution();
    },
    [addIsland, resetSolution]
  );

  const handleIslandCycleValue = useCallback(
    (id: string) => {
      cycleIslandValue(id);
      resetSolution();
    },
    [cycleIslandValue, resetSolution]
  );

  const handleIslandRightClick = useCallback(
    (id: string) => {
      removeIsland(id);
      resetSolution();
    },
    [removeIsland, resetSolution]
  );

  const handleRowsChange = useCallback(
    (newRows: number) => {
      changeRows(newRows);
      resetSolution();
    },
    [changeRows, resetSolution]
  );

  const handleColsChange = useCallback(
    (newCols: number) => {
      changeCols(newCols);
      resetSolution();
    },
    [changeCols, resetSolution]
  );

  const handleNewGrid = useCallback(() => {
    resetPuzzle();
    resetSolution();
  }, [resetPuzzle, resetSolution]);

  const handleSelectPreset = useCallback(
    (preset: Puzzle) => {
      loadPreset(preset);
      resetSolution();
    },
    [loadPreset, resetSolution]
  );

  const handleSolve = useCallback(() => {
    executeSolve(puzzle, algorithm);
  }, [executeSolve, puzzle, algorithm]);

  return (
    <div className="app-root">
      <SolverHeader
        rows={rows}
        cols={cols}
        islandCount={islands.length}
        isConnected={isConnected}
        statusText={statusText}
        onCheckConnection={checkConnection}
      />

      <div className="app-body">
        <SolverSidebar
          rows={rows}
          cols={cols}
          algorithm={algorithm}
          onRowsChange={handleRowsChange}
          onColsChange={handleColsChange}
          onAlgorithmChange={setAlgorithm}
          onNewGrid={handleNewGrid}
          onSelectPreset={handleSelectPreset}
        />

        <SolverWorkspace
          puzzle={puzzle}
          algorithm={algorithm}
          candidateBridges={candidateBridges}
          solveResult={solveResult}
          isSolving={isSolving}
          onCellClick={handleCellClick}
          onIslandRightClick={handleIslandRightClick}
          onIslandCycleValue={handleIslandCycleValue}
          onSolve={handleSolve}
        />
      </div>
    </div>
  );
}
