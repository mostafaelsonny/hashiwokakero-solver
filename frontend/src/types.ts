// Mirrors docs/DATA_MODEL.md. Field names are frozen once S1-02 is approved.
export interface Island {
  id: string;
  row: number; // 0-based, grows downward
  col: number; // 0-based, grows to the right
  required_bridges: number; // 1..8
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

export type SolveStatus =
  | "Solution Found"
  | "No Solution Exists"
  | "Search Limit Reached"
  | "No Valid Solution Found Within Search Limits"
  | "Invalid Input";

export interface SolveResult {
  status: SolveStatus;
  solution: Solution | null;
  stats: Record<string, number>;
}

export interface ValidationReport {
  valid: boolean;
  degree_violations: { island: string; required: number; actual: number }[];
  crossings: string[][];
  connected_components: number;
  invalid_values: { edge: string; value: unknown }[];
}
