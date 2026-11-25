import { useCallback, useState } from "react";
import type { Island, Puzzle } from "../types";

let _islandCounter = 0;
function nextIslandId(): string {
  _islandCounter += 1;
  return `I${_islandCounter}`;
}

function resetIslandCounter() {
  _islandCounter = 0;
}

export function usePuzzleEditor(initialRows = 7, initialCols = 7) {
  const [rows, setRows] = useState(initialRows);
  const [cols, setCols] = useState(initialCols);
  const [islands, setIslands] = useState<Island[]>([]);

  const puzzle: Puzzle = { rows, cols, islands };

  const addIsland = useCallback((row: number, col: number) => {
    setIslands((prev) => {
      if (prev.some((isl) => isl.row === row && isl.col === col)) return prev;
      const newIsland: Island = {
        id: nextIslandId(),
        row,
        col,
        required_bridges: 1,
      };
      return [...prev, newIsland];
    });
  }, []);

  const cycleIslandValue = useCallback((id: string) => {
    setIslands((prev) =>
      prev.map((isl) => {
        if (isl.id !== id) return isl;
        const next = isl.required_bridges >= 8 ? 1 : isl.required_bridges + 1;
        return { ...isl, required_bridges: next };
      })
    );
  }, []);

  const removeIsland = useCallback((id: string) => {
    setIslands((prev) => prev.filter((isl) => isl.id !== id));
  }, []);

  const resetPuzzle = useCallback(() => {
    resetIslandCounter();
    setIslands([]);
  }, []);

  const changeRows = useCallback(
    (newRows: number) => {
      setRows(newRows);
      setIslands((prev) => prev.filter((isl) => isl.row < newRows && isl.col < cols));
    },
    [cols]
  );

  const changeCols = useCallback(
    (newCols: number) => {
      setCols(newCols);
      setIslands((prev) => prev.filter((isl) => isl.row < rows && isl.col < newCols));
    },
    [rows]
  );

  const loadPreset = useCallback((preset: Puzzle) => {
    resetIslandCounter();
    setRows(preset.rows);
    setCols(preset.cols);
    setIslands(preset.islands);
  }, []);

  return {
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
  };
}
