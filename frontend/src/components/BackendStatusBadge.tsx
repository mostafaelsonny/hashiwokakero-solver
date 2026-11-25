import React from "react";

interface BackendStatusBadgeProps {
  isConnected: boolean | null;
  statusText: string;
  onCheckConnection: () => void;
}

export function BackendStatusBadge({
  isConnected,
  statusText,
  onCheckConnection,
}: BackendStatusBadgeProps) {
  return (
    <div
      className={`api-status-badge ${isConnected ? "connected" : "offline"}`}
      onClick={onCheckConnection}
      title="Click to re-verify connection to FastAPI backend"
    >
      <span>{isConnected ? "●" : "▲"}</span>
      <span>{statusText}</span>
    </div>
  );
}
