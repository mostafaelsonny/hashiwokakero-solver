import React from "react";
import { STATUS_CONFIG } from "../config/status.config";
import type { SolveResult } from "../types";

interface StatusBannerProps {
  solveResult: SolveResult;
}

export function StatusBanner({ solveResult }: StatusBannerProps) {
  const statusConfig = STATUS_CONFIG[solveResult.status] ?? STATUS_CONFIG.INVALID_RESULT;

  return (
    <div className={`solver-status-banner ${statusConfig.className}`}>
      <span className="solver-status-emoji">{statusConfig.emoji}</span>
      <div className="solver-status-body">
        <span className="solver-status-label">{statusConfig.label}</span>
        {solveResult.status === "INVALID_INPUT" && solveResult.metrics?.error && (
          <span className="solver-status-detail">{String(solveResult.metrics.error)}</span>
        )}
      </div>
    </div>
  );
}
