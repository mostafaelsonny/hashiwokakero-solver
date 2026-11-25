import type { SolveStatus } from "../types";

export const STATUS_CONFIG: Record<
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
