import React from "react";
import { ALGORITHMS } from "../config/algorithms.config";
import type { Algorithm } from "../types";
import "./ControlPanel.css";

interface AlgorithmSelectorProps {
  algorithm: Algorithm;
  onAlgorithmChange: (alg: Algorithm) => void;
}

export function AlgorithmSelector({ algorithm, onAlgorithmChange }: AlgorithmSelectorProps) {
  return (
    <div className="control-panel">
      <h3 className="control-panel-title">
        <span>🧠</span> Solving Algorithm
      </h3>

      <div className="form-group">
        <div className="radio-group">
          {ALGORITHMS.map((alg) => {
            const isActive = algorithm === alg.value;
            return (
              <label
                key={alg.value}
                className={`radio-card ${isActive ? "active" : ""}`}
              >
                <div className="radio-card-header">
                  <input
                    type="radio"
                    name="algorithm"
                    value={alg.value}
                    checked={isActive}
                    onChange={() => onAlgorithmChange(alg.value)}
                    className="radio-native"
                  />
                  <span className="radio-title">{alg.label}</span>
                </div>
                <span className="radio-desc">{alg.desc}</span>
              </label>
            );
          })}
        </div>
      </div>
    </div>
  );
}
