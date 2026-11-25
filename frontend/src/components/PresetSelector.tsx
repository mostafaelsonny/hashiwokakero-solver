import React from "react";
import { P1_PRESET, P2_PRESET } from "../config/presets";
import type { Puzzle } from "../types";

interface PresetSelectorProps {
  onSelectPreset: (preset: Puzzle) => void;
}

export function PresetSelector({ onSelectPreset }: PresetSelectorProps) {
  return (
    <div className="preset-group">
      <div className="preset-title">
        <span>📐</span> Reference Puzzles
      </div>
      <div className="preset-btn-row">
        <button
          className="preset-btn"
          onClick={() => onSelectPreset(P1_PRESET)}
          title="3x3 Grid with 4 Corner Islands (2 bridges each)"
        >
          Load P1 (3×3)
        </button>
        <button
          className="preset-btn"
          onClick={() => onSelectPreset(P2_PRESET)}
          title="3x5 Grid with Crossing Test Setup"
        >
          Load P2 (Crossing)
        </button>
      </div>
    </div>
  );
}
