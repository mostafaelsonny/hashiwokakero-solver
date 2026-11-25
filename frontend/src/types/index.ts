// Domain types — mirrors docs/DATA_MODEL.md. Field names are frozen.
export interface Island {
  id: string;
  row: number;
  col: number;
  required_bridges: number;
}

export interface Puzzle {
  rows: number;
  cols: number;
  islands: Island[];
}

export type Orientation = "horizontal" | "vertical";

export interface CandidateBridge {
  id: string;
  from: string;
  to: string;
  orientation: Orientation;
}

export interface Solution {
  bridge_counts: Record<string, 0 | 1 | 2>;
}

export type Algorithm = "backtracking" | "genetic" | "memetic";

// Canonical statuses returned by core/algorithm_runner.py
export type SolveStatus =
  | "SOLVED"
  | "UNSATISFIABLE"
  | "LIMIT_REACHED"
  | "NO_VALID_SOLUTION_FOUND"
  | "INVALID_INPUT"
  | "INVALID_RESULT";

export interface SolveResult {
  status: SolveStatus;
  solution: Solution | null;
  validation_report: ValidationReport | null;
  metrics: Record<string, number | string>;
}

export interface ValidationReport {
  valid: boolean;
  degree_violations: { island: string; required: number; actual: number }[];
  crossings: string[][];
  connected_components: number;
  invalid_values: { edge: string; value: unknown }[];
}
