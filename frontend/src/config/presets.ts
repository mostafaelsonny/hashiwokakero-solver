import type { Puzzle } from "../types";

export const P1_PRESET: Puzzle = {
  rows: 3,
  cols: 3,
  islands: [
    { id: "A", row: 0, col: 0, required_bridges: 2 },
    { id: "B", row: 0, col: 2, required_bridges: 2 },
    { id: "C", row: 2, col: 0, required_bridges: 2 },
    { id: "D", row: 2, col: 2, required_bridges: 2 },
  ],
};

export const P2_PRESET: Puzzle = {
  rows: 3,
  cols: 5,
  islands: [
    { id: "C", row: 0, col: 2, required_bridges: 1 },
    { id: "A", row: 1, col: 0, required_bridges: 1 },
    { id: "B", row: 1, col: 4, required_bridges: 1 },
    { id: "D", row: 2, col: 2, required_bridges: 1 },
  ],
};
