"use client";

import { useEffect, useRef } from "react";
import { connectSocket } from "@/lib/websocket";
import { useRealtime } from "@/store/useRealtime";
import { useAuthStore } from "@/store/authStore";
import { getAccessToken } from "@/lib/auth";

export default function useWebSocket() {
  const { addLog, addAutomation, setWsStatus, setScreenshot, setPendingConfirmation } = useRealtime();
  const { isAuthenticated } = useAuthStore();
  const wsRef = useRef<WebSocket | null>(null);
  useEffect(() => {
    const currentToken = getAccessToken();
    
    if (!isAuthenticated || !currentToken) {
        if (wsRef.current) {
            wsRef.current.close();
            wsRef.current = null;
        }
        setWsStatus("disconnected");
        return;
    }

    const ws = connectSocket(
      currentToken,
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
  }, [isAuthenticated, addLog, addAutomation, setWsStatus, setScreenshot, setPendingConfirmation]);

  return wsRef;
}
