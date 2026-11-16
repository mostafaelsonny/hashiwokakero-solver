import React from "react";
import type { Algorithm } from "../types";
import "./ControlPanel.css";

interface ControlPanelProps {
  rows: number;
  cols: number;
  algorithm: Algorithm;
  onRowsChange: (rows: number) => void;
  onColsChange: (cols: number) => void;
  onAlgorithmChange: (alg: Algorithm) => void;
  onNewGrid: () => void;
}

const ALGORITHMS: { value: Algorithm; label: string; desc: string }[] = [
  { value: "backtracking", label: "Backtracking", desc: "Exact DFS with pruning" },
  { value: "genetic", label: "Genetic Algorithm", desc: "Evolutionary heuristic" },
  { value: "memetic", label: "Memetic Algorithm", desc: "GA + local optimization" },
];

export function ControlPanel({
  rows,
  cols,
  algorithm,
  onRowsChange,
  onColsChange,
  onAlgorithmChange,
  onNewGrid,
}: ControlPanelProps) {
  return (
    <div className="control-panel">
      <h3 className="control-panel-title">
        <span>⚙️</span> Puzzle Setup
      </h3>

      {/* Grid Dimensions */}
      <div className="form-group">
        <span className="form-label">Grid Size</span>
        <div className="grid-size-row">
          <span className="number-label">Rows</span>
          <input
            type="number"
            min={2}
            max={20}
            value={rows}
            onChange={(e) => onRowsChange(Math.max(2, Math.min(20, parseInt(e.target.value) || 2)))}
            className="number-input"
          />
        </div>
        <div className="grid-size-row">
          <span className="number-label">Cols</span>
          <input
            type="number"
            min={2}
            max={20}
            value={cols}
            onChange={(e) => onColsChange(Math.max(2, Math.min(20, parseInt(e.target.value) || 2)))}
            className="number-input"
          />
        </div>
      </div>

      {/* Algorithm Selection */}
      <div className="form-group">
        <span className="form-label">Solving Algorithm</span>
        <div className="radio-group">
          {ALGORITHMS.map((alg) => {
            const isActive = algorithm === alg.value;
            return (
              <label
                key={alg.value}
                className={`radio-card ${isActive ? "active" : ""}`}
              >
                <div className="radio-card-header">
                  <input
                    type="radio"
                    name="algorithm"
                    value={alg.value}
                    checked={isActive}
                    onChange={() => onAlgorithmChange(alg.value)}
                    className="radio-native"
                  />
                  <span className="radio-title">{alg.label}</span>
                </div>
                <span className="radio-desc">{alg.desc}</span>
              </label>
            );
          })}
        </div>
      </div>

      {/* Reset Button */}
      <button onClick={onNewGrid} className="btn-reset">
        <span>🔄</span> Reset Grid
      </button>
    </div>
  );
}
