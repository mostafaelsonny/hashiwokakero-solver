import React, { useState } from "react";
import { getCandidateBridges, validate } from "../api/solver.api";
import { P1_PRESET, P2_PRESET } from "../config/presets";
import type { Puzzle } from "../types";

interface BackendDebugPanelProps {
  puzzle: Puzzle;
}

export function BackendDebugPanel({ puzzle }: BackendDebugPanelProps) {
  const [testResult, setTestResult] = useState<{ title: string; data: unknown } | null>(null);
  const [isLoading, setIsLoading] = useState(false);

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
    if (puzzle.islands.length === 0) {
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
        title: `POST /validate (Dynamic Active Grid: ${puzzle.islands.length} islands)`,
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

  return (
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
  );
}
