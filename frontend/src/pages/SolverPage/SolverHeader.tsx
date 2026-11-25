import React from "react";
import { BackendStatusBadge } from "../../components/BackendStatusBadge";

interface SolverHeaderProps {
  rows: number;
  cols: number;
  islandCount: number;
  isConnected: boolean | null;
  statusText: string;
  onCheckConnection: () => void;
}

export function SolverHeader({
  rows,
  cols,
  islandCount,
  isConnected,
  statusText,
  onCheckConnection,
}: SolverHeaderProps) {
  return (
    <header className="app-header">
      <h1 className="app-header-title">
        <span>♟️</span> Hashiwokakero Solver
      </h1>
      <span className="sprint-badge">Sprint 2</span>

      <BackendStatusBadge
        isConnected={isConnected}
        statusText={statusText}
        onCheckConnection={onCheckConnection}
      />

      <span className="header-sub">
        Puzzle Editor · {rows}×{cols} Board · {islandCount} Islands
      </span>
    </header>
  );
}
