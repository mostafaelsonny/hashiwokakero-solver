import React, { useCallback, useEffect, useState } from "react";
import type { Algorithm, CandidateBridge, Island, Puzzle, SolveResult, SolveStatus } from "./types";
import { ControlPanel } from "./components/ControlPanel";
import { PuzzleGrid } from "./components/PuzzleGrid";
import { JsonPreview } from "./components/JsonPreview";
import { checkHealth, getCandidateBridges, solve, validate } from "./api";
import "./App.css";

// ---------------------------------------------------------------------------
// Helpers & Standard Fixtures
// ---------------------------------------------------------------------------

let _islandCounter = 0;
function nextIslandId(): string {
  _islandCounter += 1;
  return `I${_islandCounter}`;
}

function resetIslandCounter() {
  _islandCounter = 0;
}

const P1_PRESET: Puzzle = {
  rows: 3,
  cols: 3,
  islands: [
    { id: "A", row: 0, col: 0, required_bridges: 2 },
    { id: "B", row: 0, col: 2, required_bridges: 2 },
    { id: "C", row: 2, col: 0, required_bridges: 2 },
    { id: "D", row: 2, col: 2, required_bridges: 2 },
  ],
};

const P2_PRESET: Puzzle = {
  rows: 3,
  cols: 5,
  islands: [
    { id: "C", row: 0, col: 2, required_bridges: 1 },
    { id: "A", row: 1, col: 0, required_bridges: 1 },
    { id: "B", row: 1, col: 4, required_bridges: 1 },
    { id: "D", row: 2, col: 2, required_bridges: 1 },
  ],
};

// ---------------------------------------------------------------------------
// Status Banner Config
// ---------------------------------------------------------------------------

const STATUS_CONFIG: Record<
  SolveStatus,
  { emoji: string; label: string; className: string }
> = {
  SOLVED: { emoji: "✅", label: "Puzzle Solved!", className: "status-solved" },
  UNSATISFIABLE: { emoji: "🚫", label: "No Solution Exists (UNSATISFIABLE)", className: "status-error" },
  LIMIT_REACHED: { emoji: "⏱️", label: "Search Limit Reached – try increasing limits", className: "status-warn" },
  NO_VALID_SOLUTION_FOUND: { emoji: "🔍", label: "No Valid Solution Found Within Search Limits", className: "status-warn" },
  INVALID_INPUT: { emoji: "⚠️", label: "Invalid Input", className: "status-error" },
  INVALID_RESULT: { emoji: "🐛", label: "Internal Error: Solver returned invalid result", className: "status-error" },
};

// ---------------------------------------------------------------------------
// App Component
// ---------------------------------------------------------------------------

export default function App() {
  const [rows, setRows] = useState(7);
  const [cols, setCols] = useState(7);
  const [islands, setIslands] = useState<Island[]>([]);
  const [algorithm, setAlgorithm] = useState<Algorithm>("backtracking");

  // API State
  const [apiConnected, setApiConnected] = useState<boolean | null>(null);
  const [apiStatusText, setApiStatusText] = useState("Checking...");
  const [testResult, setTestResult] = useState<{ title: string; data: unknown } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Solver State
  const [solveResult, setSolveResult] = useState<SolveResult | null>(null);
  const [candidateBridges, setCandidateBridges] = useState<CandidateBridge[]>([]);
  const [isSolving, setIsSolving] = useState(false);

  const puzzle: Puzzle = { rows, cols, islands };

  // Check health on mount
  const verifyBackendHealth = useCallback(async () => {
    try {
      setApiStatusText("Checking API...");
      const res = await checkHealth();
      if (res.status === "ok") {
        setApiConnected(true);
        setApiStatusText("Backend Connected (200 OK)");
      } else {
        setApiConnected(false);
        setApiStatusText("Unexpected Status");
      }
    } catch {
      setApiConnected(false);
      setApiStatusText("Backend Offline (Run uvicorn)");
    }
  }, []);

  useEffect(() => {
    verifyBackendHealth();
  }, [verifyBackendHealth]);

  // Handlers for Grid Editing
  const handleCellClick = useCallback((row: number, col: number) => {
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
    // Clear any existing solution when puzzle changes
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  const handleIslandCycleValue = useCallback((id: string) => {
    setIslands((prev) =>
      prev.map((isl) => {
        if (isl.id !== id) return isl;
        const next = isl.required_bridges >= 8 ? 1 : isl.required_bridges + 1;
        return { ...isl, required_bridges: next };
      })
    );
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  const handleIslandRightClick = useCallback((id: string) => {
    setIslands((prev) => prev.filter((isl) => isl.id !== id));
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  const handleNewGrid = useCallback(() => {
    resetIslandCounter();
    setIslands([]);
    setTestResult(null);
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  const handleRowsChange = useCallback((newRows: number) => {
    setRows(newRows);
    setIslands((prev) => prev.filter((isl) => isl.row < newRows && isl.col < cols));
    setSolveResult(null);
    setCandidateBridges([]);
  }, [cols]);

  const handleColsChange = useCallback((newCols: number) => {
    setCols(newCols);
    setIslands((prev) => prev.filter((isl) => isl.row < rows && isl.col < newCols));
    setSolveResult(null);
    setCandidateBridges([]);
  }, [rows]);

  // Load Presets
  const loadPreset = useCallback((preset: Puzzle) => {
    resetIslandCounter();
    setRows(preset.rows);
    setCols(preset.cols);
    setIslands(preset.islands);
    setTestResult(null);
    setSolveResult(null);
    setCandidateBridges([]);
  }, []);

  // -------------------------------------------------------------------------
  // 🚀 Main Solve Handler
  // -------------------------------------------------------------------------
  const handleSolve = async () => {
    if (islands.length === 0) return;
    setIsSolving(true);
    setSolveResult(null);
    setCandidateBridges([]);

    try {
      // Fetch candidate bridges for rendering
      const bridgesRes = await getCandidateBridges(puzzle);
      setCandidateBridges(bridgesRes.candidate_bridges);

      // Call solver
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
  };

  // -------------------------------------------------------------------------
  // Legacy API Test Actions (kept for debugging)
  // -------------------------------------------------------------------------
  const handleTestCandidateBridges = async () => {
    setIsLoading(true);
    try {
      const res = await getCandidateBridges(puzzle);
      setTestResult({
        title: `POST /candidate-bridges (${res.candidate_bridges.length} candidate edges found)`,
        data: res,
      });
    } catch (err: unknown) {
      setTestResult({
        title: "POST /candidate-bridges Error",
        data: String(err),
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestValidateCurrentGrid = async () => {
    if (islands.length === 0) {
      setTestResult({
        title: "Active Grid Validation",
        data: "Please place at least one island on the grid or load a preset!",
      });
      return;
    }
    setIsLoading(true);
    try {
      const res = await validate(puzzle, { bridge_counts: {} });
      setTestResult({
        title: `POST /validate (Dynamic Active Grid: ${islands.length} islands)`,
        data: res,
      });
    } catch (err: unknown) {
      setTestResult({ title: "Validation Error", data: String(err) });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestValidateP1Valid = async () => {
    setIsLoading(true);
    try {
      const solution = {
        bridge_counts: { E1: 1 as const, E2: 1 as const, E3: 1 as const, E4: 1 as const },
      };
      const res = await validate(P1_PRESET, solution);
      setTestResult({
        title: "POST /validate (P1 with Valid Solution [1,1,1,1])",
        data: res,
      });
    } catch (err: unknown) {
      setTestResult({ title: "Validation Error", data: String(err) });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestValidateDegreeViolation = async () => {
    setIsLoading(true);
    try {
      const solution = {
        bridge_counts: { E1: 1 as const, E2: 0 as const, E3: 1 as const, E4: 1 as const },
      };
      const res = await validate(P1_PRESET, solution);
      setTestResult({
        title: "POST /validate (P1 with Missing Bridge [1,0,1,1] - Degree Violation)",
        data: res,
      });
    } catch (err: unknown) {
      setTestResult({ title: "Validation Error", data: String(err) });
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestValidateCrossing = async () => {
    setIsLoading(true);
    try {
      const solution = {
        bridge_counts: { E1: 1 as const, E2: 1 as const },
      };
      const res = await validate(P2_PRESET, solution);
      setTestResult({
        title: "POST /validate (P2 with Crossing Bridges [1,1] - Crossing Violation)",
        data: res,
      });
    } catch (err: unknown) {
      setTestResult({ title: "Validation Error", data: String(err) });
    } finally {
      setIsLoading(false);
    }
  };

  // -------------------------------------------------------------------------
  // Render helpers
  // -------------------------------------------------------------------------
  const statusConfig = solveResult ? STATUS_CONFIG[solveResult.status] ?? STATUS_CONFIG.INVALID_RESULT : null;

  const metricEntries = solveResult?.metrics
    ? Object.entries(solveResult.metrics).filter(([, v]) => typeof v === "number")
    : [];

  return (
    <div className="app-root">
      {/* Header */}
      <header className="app-header">
        <h1 className="app-header-title">
          <span>♟️</span> Hashiwokakero Solver
        </h1>
        <span className="sprint-badge">Sprint 2</span>

        {/* Backend API Live Status Badge */}
        <div
          className={`api-status-badge ${apiConnected ? "connected" : "offline"}`}
          onClick={verifyBackendHealth}
          title="Click to re-verify connection to FastAPI backend"
        >
          <span>{apiConnected ? "●" : "▲"}</span>
          <span>{apiStatusText}</span>
        </div>

        <span className="header-sub">
          Puzzle Editor · {rows}×{cols} Board · {islands.length} Islands
        </span>
      </header>

      {/* Body */}
      <div className="app-body">
        {/* Sidebar */}
        <aside className="app-sidebar">
          {/* Quick Presets */}
          <div className="preset-group">
            <div className="preset-title">
              <span>📐</span> Reference Puzzles
            </div>
            <div className="preset-btn-row">
              <button
                className="preset-btn"
                onClick={() => loadPreset(P1_PRESET)}
                title="3x3 Grid with 4 Corner Islands (2 bridges each)"
              >
                Load P1 (3×3)
              </button>
              <button
                className="preset-btn"
                onClick={() => loadPreset(P2_PRESET)}
                title="3x5 Grid with Crossing Test Setup"
              >
                Load P2 (Crossing)
              </button>
            </div>
          </div>

          <ControlPanel
            rows={rows}
            cols={cols}
            algorithm={algorithm}
            onRowsChange={handleRowsChange}
            onColsChange={handleColsChange}
            onAlgorithmChange={setAlgorithm}
            onNewGrid={handleNewGrid}
          />

          {/* Quick Guide */}
          <div className="quick-guide-card">
            <div className="quick-guide-title">
              <span>📖</span> How to Play / Edit
            </div>
            <ul className="quick-guide-list">
              <li>
                <b>Click square</b> → Place island (value = 1)
              </li>
              <li>
                <b>Click island</b> → Cycle value 1 → 2 → … → 8 → 1
              </li>
              <li>
                <b>Right-click island</b> → Remove island
              </li>
              <li>Change <b>Rows/Cols</b> to resize board</li>
              <li>
                Click <b>Reset Grid</b> to clear
              </li>
            </ul>
          </div>
        </aside>

        {/* Main Grid Area */}
        <main className="app-main">
          <PuzzleGrid
            rows={rows}
            cols={cols}
            islands={islands}
            candidateBridges={candidateBridges}
            solvedBridgeCounts={solveResult?.solution?.bridge_counts ?? null}
            onCellClick={handleCellClick}
            onIslandRightClick={handleIslandRightClick}
            onIslandCycleValue={handleIslandCycleValue}
          />

          <p className="hint-text">
            {islands.length === 0
              ? "👉 Click any square on the board or load a preset (P1 / P2) to begin."
              : `✓ ${islands.length} island${islands.length !== 1 ? "s" : ""} placed. Click to cycle bridge counts (1-8), right-click to remove.`}
          </p>

          {/* ================================================================
              🚀 SOLVER PANEL (Sprint 2 Main Feature)
              ================================================================ */}
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
              onClick={handleSolve}
              disabled={isSolving || islands.length === 0}
            >
              {isSolving ? (
                <><span>⏳</span> Solving…</>
              ) : (
                <><span>🚀</span> Solve with {algorithm.charAt(0).toUpperCase() + algorithm.slice(1)}</>
              )}
            </button>

            {/* Status Banner */}
            {solveResult && statusConfig && (
              <div className={`solver-status-banner ${statusConfig.className}`}>
                <span className="solver-status-emoji">{statusConfig.emoji}</span>
                <div className="solver-status-body">
                  <span className="solver-status-label">{statusConfig.label}</span>
                  {solveResult.status === "INVALID_INPUT" && solveResult.metrics?.error && (
                    <span className="solver-status-detail">{String(solveResult.metrics.error)}</span>
                  )}
                </div>
              </div>
            )}

            {/* Metrics */}
            {solveResult && metricEntries.length > 0 && (
              <div className="metrics-grid">
                <div className="metrics-title">📊 Execution Metrics</div>
                <div className="metrics-entries">
                  {metricEntries.map(([key, val]) => (
                    <div key={key} className="metric-item">
                      <span className="metric-key">{key.replace(/_/g, " ")}</span>
                      <span className="metric-val">
                        {typeof val === "number" && key.includes("ms")
                          ? `${Number(val).toFixed(1)} ms`
                          : typeof val === "number"
                          ? Number(val).toLocaleString()
                          : String(val)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Raw JSON (collapsed view) */}
            {solveResult && (
              <details className="result-details">
                <summary className="result-details-summary">🔍 Raw API Response</summary>
                <pre className="result-content">
                  {JSON.stringify(solveResult, null, 2)}
                </pre>
              </details>
            )}
          </section>

          {/* Backend API Debug Testing Panel */}
          <section className="test-panel">
            <div className="test-panel-header">
              <h3 className="test-panel-title">
                <span>🧪</span> Backend API Debug Tests
              </h3>
              <span className="test-panel-sub">
                Sprint 1 Verification Endpoints
              </span>
            </div>

            <div className="test-buttons-row">
              <button
                className="btn-action-primary"
                onClick={handleTestCandidateBridges}
                disabled={isLoading}
              >
                <span>🌉</span> 1. Test /candidate-bridges
              </button>

              <button
                className="btn-action-primary highlight"
                onClick={handleTestValidateCurrentGrid}
                disabled={isLoading}
              >
                <span>🎯</span> 2. Validate My Active Grid
              </button>

              <button
                className="btn-action-secondary"
                onClick={handleTestValidateP1Valid}
                disabled={isLoading}
              >
                <span>✅</span> P1 Preset [1,1,1,1]
              </button>

              <button
                className="btn-action-secondary"
                onClick={handleTestValidateDegreeViolation}
                disabled={isLoading}
              >
                <span>⚠️</span> P1 Missing Bridge [1,0,1,1]
              </button>

              <button
                className="btn-action-secondary"
                onClick={handleTestValidateCrossing}
                disabled={isLoading}
              >
                <span>⚔️</span> P2 Crossing [1,1]
              </button>
            </div>

            {testResult && (
              <div className="result-box">
                <div className="result-title">
                  <span>{testResult.title}</span>
                  <span className="result-badge">API Response</span>
                </div>
                <pre className="result-content">
                  {typeof testResult.data === "string"
                    ? testResult.data
                    : JSON.stringify(testResult.data, null, 2)}
                </pre>
              </div>
            )}
          </section>

          {/* JSON Live Preview */}
          <JsonPreview puzzle={puzzle} />
        </main>
      </div>
    </div>
  );
}
