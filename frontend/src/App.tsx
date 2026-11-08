// Layout skeleton only. S1-11 (Puzzle Editor) fills these zones; later sprints add results/visualization.
const zone: React.CSSProperties = {
  border: "1px dashed #999",
  borderRadius: 8,
  padding: 16,
  minHeight: 120,
};

export default function App() {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", maxWidth: 960, margin: "0 auto", padding: 24 }}>
      <h1>Hashiwokakero Solver</h1>
      <section style={zone}>
        <h2>1. Puzzle Editor (S1-11)</h2>
        <p>Rows / Columns, click a cell to add an island, set its number (1-8).</p>
      </section>
      <section style={{ ...zone, marginTop: 16 }}>
        <h2>2. Algorithm Selection</h2>
        <p>Backtracking / Genetic Algorithm / Memetic Algorithm.</p>
      </section>
      <section style={{ ...zone, marginTop: 16 }}>
        <h2>3. Visualization (SVG)</h2>
        <p>Islands, bridges, double bridges, final solution.</p>
      </section>
      <section style={{ ...zone, marginTop: 16 }}>
        <h2>4. Results</h2>
        <p>Status, execution time, validation report.</p>
      </section>
    </main>
  );
}
