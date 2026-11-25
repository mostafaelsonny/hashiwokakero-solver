import React from "react";

interface MetricsGridProps {
  metrics: Record<string, number | string>;
}

export function MetricsGrid({ metrics }: MetricsGridProps) {
  const metricEntries = Object.entries(metrics).filter(([, v]) => typeof v === "number");
  if (metricEntries.length === 0) return null;

  return (
    <div className="metrics-grid">
      <div className="metrics-title">📊 Execution Metrics</div>
      <div className="metrics-entries">
        {metricEntries.map(([key, val]) => (
          <div key={key} className="metric-item">
            <span className="metric-key">{key.replace(/_/g, " ")}</span>
            <span className="metric-val">
              {typeof val === "number" && key.includes("ms")
                ? `${Number(val).toFixed(1)} ms`
                : typeof val === "number"
                ? Number(val).toLocaleString()
                : String(val)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
