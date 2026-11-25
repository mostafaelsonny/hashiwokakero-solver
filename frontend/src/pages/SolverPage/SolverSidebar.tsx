import React from "react";
import { AlgorithmSelector } from "../../components/AlgorithmSelector";
import { PresetSelector } from "../../components/PresetSelector";
import { PuzzleSettings } from "../../components/PuzzleSettings";
import { QuickGuide } from "../../components/QuickGuide";
import type { Algorithm, Puzzle } from "../../types";

interface SolverSidebarProps {
  rows: number;
  cols: number;
  algorithm: Algorithm;
  onRowsChange: (rows: number) => void;
  onColsChange: (cols: number) => void;
  onAlgorithmChange: (alg: Algorithm) => void;
  onNewGrid: () => void;
  onSelectPreset: (preset: Puzzle) => void;
}

export function SolverSidebar({
  rows,
  cols,
  algorithm,
  onRowsChange,
  onColsChange,
  onAlgorithmChange,
  onNewGrid,
  onSelectPreset,
}: SolverSidebarProps) {
  return (
    <aside className="app-sidebar">
      <PresetSelector onSelectPreset={onSelectPreset} />

      <PuzzleSettings
        rows={rows}
        cols={cols}
        onRowsChange={onRowsChange}
        onColsChange={onColsChange}
        onNewGrid={onNewGrid}
      />

      <AlgorithmSelector
        algorithm={algorithm}
        onAlgorithmChange={onAlgorithmChange}
      />

      <QuickGuide />
    </aside>
  );
}
