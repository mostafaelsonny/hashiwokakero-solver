// Reference puzzle P1 (see docs/DATA_MODEL.md). The only valid solution is [1,1,1,1].
import type { Puzzle } from "./types";

export const P1: Puzzle = {
  rows: 3,
  cols: 3,
  islands: [
    { id: "A", row: 0, col: 0, required_bridges: 2 },
    { id: "B", row: 0, col: 2, required_bridges: 2 },
    { id: "C", row: 2, col: 0, required_bridges: 2 },
    { id: "D", row: 2, col: 2, required_bridges: 2 },
  ],
};
