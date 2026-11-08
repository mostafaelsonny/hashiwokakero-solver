import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In dev, /api/* is forwarded to the FastAPI server (uvicorn api.main:app --reload).
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
});
