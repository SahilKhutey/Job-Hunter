"use client";

import { useEffect, useRef } from "react";
import { connectSocket } from "@/lib/websocket";
import { useRealtime } from "@/store/useRealtime";
import { useAuth } from "@/store/useAuth";

export default function useWebSocket() {
  const { addLog, addAutomation, setWsStatus, setScreenshot, setPendingConfirmation } = useRealtime();
  const { token, isAuthenticated } = useAuth();
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!isAuthenticated || !token) {
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
        return;
    }

    const ws = connectSocket(
      token,
      (data) => {
        if (data.type === "agent_update") {
          addLog({ agent: data.agent, status: data.status, message: data.message });
        }
        if (data.type === "automation") {
          addAutomation({ step: data.step, status: data.status });
        }
        if (data.type === "browser_view") {
          setScreenshot(data.image);
        }
        if (data.type === "awaiting_confirmation") {
          setPendingConfirmation(data.job_id);
        }
      },
      setWsStatus
    );

    wsRef.current = ws;
    return () => {
      wsRef.current?.close();
    };
  }, [isAuthenticated, token, addLog, addAutomation, setWsStatus, setScreenshot, setPendingConfirmation]);

  return wsRef;
}
