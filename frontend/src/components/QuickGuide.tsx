import React from "react";

export function QuickGuide() {
  return (
    <div className="quick-guide-card">
      <div className="quick-guide-title">
        <span>📖</span> How to Play / Edit
      </div>
      <ul className="quick-guide-list">
        <li>
          <b>Click square</b> → Place island (value = 1)
        </li>
        <li>
          <b>Click island</b> → Cycle value 1 → 2 → … → 8 → 1
        </li>
        <li>
          <b>Right-click island</b> → Remove island
        </li>
        <li>Change <b>Rows/Cols</b> to resize board</li>
        <li>
          Click <b>Reset Grid</b> to clear
        </li>
      </ul>
    </div>
  );
}
