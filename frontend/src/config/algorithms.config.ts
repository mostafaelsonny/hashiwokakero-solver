import type { Algorithm } from "../types";

export const ALGORITHMS: { value: Algorithm; label: string; desc: string }[] = [
  { value: "backtracking", label: "Backtracking", desc: "Exact DFS with pruning" },
  { value: "genetic", label: "Genetic Algorithm", desc: "Evolutionary heuristic" },
  { value: "memetic", label: "Memetic Algorithm", desc: "GA + local optimization" },
];
