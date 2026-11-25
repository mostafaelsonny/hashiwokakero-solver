import React from "react";
import type { Algorithm, SolveResult } from "../types";
import { MetricsGrid } from "./MetricsGrid";
import { StatusBanner } from "./StatusBanner";

interface SolverPanelProps {
  algorithm: Algorithm;
  isSolving: boolean;
  hasIslands: boolean;
  solveResult: SolveResult | null;
  onSolve: () => void;
}

export function SolverPanel({
  algorithm,
  isSolving,
  hasIslands,
  solveResult,
  onSolve,
}: SolverPanelProps) {
  return (
    <section className="solver-panel">
      <div className="test-panel-header">
        <h3 className="test-panel-title">
          <span>🤖</span> Solve Puzzle
        </h3>
        <span className="test-panel-sub">
          Algorithm: <strong>{algorithm}</strong>
        </span>
      </div>

      <button
        className="btn-solve"
        onClick={onSolve}
        disabled={isSolving || !hasIslands}
      >
        {isSolving ? (
          <><span>⏳</span> Solving…</>
        ) : (
          <><span>🚀</span> Solve with {algorithm.charAt(0).toUpperCase() + algorithm.slice(1)}</>
        )}
      </button>

      {solveResult && <StatusBanner solveResult={solveResult} />}

      {solveResult?.metrics && <MetricsGrid metrics={solveResult.metrics} />}

      {solveResult && (
        <details className="result-details">
          <summary className="result-details-summary">🔍 Raw API Response</summary>
          <pre className="result-content">
            {JSON.stringify(solveResult, null, 2)}
          </pre>
        </details>
      )}
    </section>
  );
}
