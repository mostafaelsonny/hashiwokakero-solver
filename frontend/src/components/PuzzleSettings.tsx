import React from "react";
import "./ControlPanel.css";

interface PuzzleSettingsProps {
  rows: number;
  cols: number;
  onRowsChange: (rows: number) => void;
  onColsChange: (cols: number) => void;
  onNewGrid: () => void;
}

export function PuzzleSettings({
  rows,
  cols,
  onRowsChange,
  onColsChange,
  onNewGrid,
}: PuzzleSettingsProps) {
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

      {/* Reset Button */}
      <button onClick={onNewGrid} className="btn-reset">
        <span>🔄</span> Reset Grid
      </button>
    </div>
  );
}
