import React from "react";
import type { CandidateBridge, Island } from "../types";
import "./PuzzleGrid.css";

interface PuzzleGridProps {
  rows: number;
  cols: number;
  islands: Island[];
  candidateBridges: CandidateBridge[];
  solvedBridgeCounts: Record<string, 0 | 1 | 2> | null;
  onCellClick: (row: number, col: number) => void;
  onIslandRightClick: (id: string) => void;
  onIslandCycleValue: (id: string) => void;
}

const CELL_SIZE = 60;
const ISLAND_RADIUS = 21;
const PADDING = 34;
const BRIDGE_GAP = 5; // pixel offset for double bridge lines

function getIslandAt(islands: Island[], row: number, col: number): Island | undefined {
  return islands.find((isl) => isl.row === row && isl.col === col);
}

function getIslandById(islands: Island[], id: string): Island | undefined {
  return islands.find((isl) => isl.id === id);
}

export function PuzzleGrid({
  rows,
  cols,
  islands,
  candidateBridges,
  solvedBridgeCounts,
  onCellClick,
  onIslandRightClick,
  onIslandCycleValue,
}: PuzzleGridProps) {
  const svgWidth = cols * CELL_SIZE + PADDING * 2;
  const svgHeight = rows * CELL_SIZE + PADDING * 2;

  function cellCenter(row: number, col: number): [number, number] {
    return [PADDING + col * CELL_SIZE + CELL_SIZE / 2, PADDING + row * CELL_SIZE + CELL_SIZE / 2];
  }

  // Build bridge rendering data
  const bridgeLines: React.ReactNode[] = [];

  if (candidateBridges.length > 0 && solvedBridgeCounts) {
    for (const edge of candidateBridges) {
      const count = solvedBridgeCounts[edge.id] as number | undefined;
      if (!count) continue;

      const fromIsland = getIslandById(islands, edge.from);
      const toIsland = getIslandById(islands, edge.to);
      if (!fromIsland || !toIsland) continue;

      const [x1, y1] = cellCenter(fromIsland.row, fromIsland.col);
      const [x2, y2] = cellCenter(toIsland.row, toIsland.col);

      if (count === 1) {
        bridgeLines.push(
          <line
            key={`bridge-${edge.id}`}
            x1={x1}
            y1={y1}
            x2={x2}
            y2={y2}
            className="bridge-single"
          />
        );
      } else {
        // Double bridge: draw two parallel lines offset perpendicular to the direction
        const isHorizontal = edge.orientation === "horizontal";
        const dx = isHorizontal ? 0 : BRIDGE_GAP;
        const dy = isHorizontal ? BRIDGE_GAP : 0;

        bridgeLines.push(
          <React.Fragment key={`bridge-${edge.id}`}>
            <line
              x1={x1 - dx}
              y1={y1 - dy}
              x2={x2 - dx}
              y2={y2 - dy}
              className="bridge-double"
            />
            <line
              x1={x1 + dx}
              y1={y1 + dy}
              x2={x2 + dx}
              y2={y2 + dy}
              className="bridge-double"
            />
          </React.Fragment>
        );
      }
    }
  }

  return (
    <div className="puzzle-grid-container">
      <div className="chess-board-frame">
        <svg
          width={svgWidth}
          height={svgHeight}
          className="puzzle-grid-svg"
        >
          <defs>
            <filter id="island-shadow" x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0" dy="3" stdDeviation="3" floodColor="#3a200a" floodOpacity="0.35" />
            </filter>
          </defs>

          {/* Board Outer Border */}
          <rect
            x={PADDING - 8}
            y={PADDING - 8}
            width={cols * CELL_SIZE + 16}
            height={rows * CELL_SIZE + 16}
            className="board-outer-border"
          />

          {/* Checkered cells */}
          {Array.from({ length: rows }, (_, r) =>
            Array.from({ length: cols }, (_, c) => {
              const [cx, cy] = cellCenter(r, c);
              const isAlternate = (r + c) % 2 === 1;
              return (
                <rect
                  key={`cell-${r}-${c}`}
                  x={cx - CELL_SIZE / 2}
                  y={cy - CELL_SIZE / 2}
                  width={CELL_SIZE}
                  height={CELL_SIZE}
                  className={`grid-cell ${isAlternate ? "cell-dark" : "cell-light"}`}
                  onClick={() => {
                    const existing = getIslandAt(islands, r, c);
                    if (existing) {
                      onIslandCycleValue(existing.id);
                    } else {
                      onCellClick(r, c);
                    }
                  }}
                />
              );
            })
          )}

          {/* Center dots */}
          {Array.from({ length: rows }, (_, r) =>
            Array.from({ length: cols }, (_, c) => {
              const [cx, cy] = cellCenter(r, c);
              const hasIsland = !!getIslandAt(islands, r, c);
              if (hasIsland) return null;
              return (
                <circle
                  key={`dot-${r}-${c}`}
                  cx={cx}
                  cy={cy}
                  r={2.5}
                  className="grid-center-dot"
                />
              );
            })
          )}

          {/* 🌉 Bridge Lines (rendered BELOW islands so islands appear on top) */}
          {bridgeLines}

          {/* Islands */}
          {islands.map((island) => {
            const [cx, cy] = cellCenter(island.row, island.col);
            return (
              <g
                key={island.id}
                className="island-group"
                onClick={() => onIslandCycleValue(island.id)}
                onContextMenu={(e) => {
                  e.preventDefault();
                  onIslandRightClick(island.id);
                }}
              >
                {/* Accent ring */}
                <circle
                  cx={cx}
                  cy={cy}
                  r={ISLAND_RADIUS + 3}
                  className="island-halo"
                />
                {/* Island piece */}
                <circle
                  cx={cx}
                  cy={cy}
                  r={ISLAND_RADIUS}
                  className="island-circle"
                  filter="url(#island-shadow)"
                />
                {/* Required bridges number */}
                <text
                  x={cx}
                  y={cy + 6}
                  className="island-value-text"
                >
                  {island.required_bridges}
                </text>
                {/* Island ID tag */}
                <text
                  x={cx}
                  y={cy + ISLAND_RADIUS + 13}
                  className="island-id-text"
                >
                  {island.id}
                </text>
              </g>
            );
          })}

          {/* Empty hint */}
          {islands.length === 0 && (
            <text
              x={svgWidth / 2}
              y={svgHeight / 2}
              className="grid-empty-hint"
            >
              Click any square to place an island
            </text>
          )}
        </svg>
      </div>
    </div>
  );
}
