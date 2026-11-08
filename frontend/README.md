# Frontend

React + TypeScript + Vite. Sprint 1 task **S1-11**: Basic Puzzle Editor (input and display only; no algorithm yet).

```bash
npm install
npm run dev      # http://localhost:5173  (calls to /api/* are proxied to FastAPI on :8000)
npm run build
npm test
```

- `src/types.ts` mirrors `docs/DATA_MODEL.md`. The JSON the editor outputs must match it **by the letter** (`required_bridges`, ...).
- `src/api.ts` has `solve()` and `validate()` for later sprints.
- `src/fixtures.ts` has puzzle P1 for quick manual tests.
- `src/App.tsx` is just a layout skeleton: replace the zones with real components.
