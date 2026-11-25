import { describe, expect, it } from "vitest";
import { P1 } from "./fixtures";

describe("P1 fixture", () => {
  it("has an even sum of required bridges (necessary condition)", () => {
    const sum = P1.islands.reduce((total, island) => total + island.required_bridges, 0);
    expect(sum % 2).toBe(0);
  });

  it("keeps every island inside the grid", () => {
    for (const island of P1.islands) {
      expect(island.row).toBeLessThan(P1.rows);
      expect(island.col).toBeLessThan(P1.cols);
    }
  });
});
