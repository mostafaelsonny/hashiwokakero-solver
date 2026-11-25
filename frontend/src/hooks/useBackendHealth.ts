import { useCallback, useEffect, useState } from "react";
import { checkHealth } from "../api/health.api";

export function useBackendHealth() {
  const [isConnected, setIsConnected] = useState<boolean | null>(null);
  const [statusText, setStatusText] = useState("Checking...");

  const checkConnection = useCallback(async () => {
    try {
      setStatusText("Checking API...");
      const res = await checkHealth();
      if (res.status === "ok") {
        setIsConnected(true);
        setStatusText("Backend Connected (200 OK)");
      } else {
        setIsConnected(false);
        setStatusText("Unexpected Status");
      }
    } catch {
      setIsConnected(false);
      setStatusText("Backend Offline (Run uvicorn)");
    }
  }, []);

  useEffect(() => {
    checkConnection();
  }, [checkConnection]);

  return {
    isConnected,
    statusText,
    checkConnection,
  };
}
