import React from "react";
import type { Puzzle } from "../types";
import "./JsonPreview.css";

interface JsonPreviewProps {
  puzzle: Puzzle;
}

export function JsonPreview({ puzzle }: JsonPreviewProps) {
  const json = JSON.stringify(puzzle, null, 2);
  const islandCount = puzzle.islands.length;

  return (
    <div className="json-preview-container">
      <div className="json-preview-header">
        <span className="json-preview-title">
          <span>📋</span> Puzzle JSON (Data Model)
        </span>
        <span className="json-preview-badge">
          {islandCount} island{islandCount !== 1 ? "s" : ""}
        </span>
      </div>
      <pre className="json-preview-code">{json}</pre>
    </div>
  );
}
