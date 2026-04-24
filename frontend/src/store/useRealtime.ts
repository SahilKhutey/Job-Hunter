import { create } from "zustand";

export interface AgentLog {
  id: string;
  agent: string;
  status: string;
  message: string;
  timestamp: string;
}

export interface AutomationStep {
  id: string;
  step: string;
  status: "running" | "done" | "error";
  timestamp: string;
}

interface RealtimeState {
  logs: AgentLog[];
  automation: AutomationStep[];
  currentScreenshot: string | null;
  wsStatus: "connecting" | "connected" | "disconnected" | "error";
  pendingConfirmation: string | null;
  addLog: (log: Omit<AgentLog, "id" | "timestamp">) => void;
  addAutomation: (step: Omit<AutomationStep, "id" | "timestamp">) => void;
  updateAutomationStep: (step: string, status: AutomationStep["status"]) => void;
  setScreenshot: (base64: string | null) => void;
  setWsStatus: (status: RealtimeState["wsStatus"]) => void;
  setPendingConfirmation: (jobId: string | null) => void;
  clearAll: () => void;
}

export const useRealtime = create<RealtimeState>((set) => ({
  logs: [],
  automation: [],
  currentScreenshot: null,
  wsStatus: "connecting",
  pendingConfirmation: null,

  addLog: (log) =>
    set((state) => ({
      logs: [
        {
          ...log,
          id: Math.random().toString(36).slice(2),
          timestamp: new Date().toLocaleTimeString(),
        },
        ...state.logs.slice(0, 99), // Cap at 100 logs
      ],
    })),

  addAutomation: (step) =>
    set((state) => ({
      automation: [
        ...state.automation,
        {
          ...step,
          id: Math.random().toString(36).slice(2),
          timestamp: new Date().toLocaleTimeString(),
        },
      ].slice(-50), // Cap at 50 steps
    })),

  updateAutomationStep: (step, status) =>
    set((state) => ({
      automation: state.automation.map((s) =>
        s.step === step ? { ...s, status } : s
      ),
    })),

  setScreenshot: (currentScreenshot) => set({ currentScreenshot }),

  setWsStatus: (wsStatus) => set({ wsStatus }),

  setPendingConfirmation: (pendingConfirmation) => set({ pendingConfirmation }),

  clearAll: () => set({ logs: [], automation: [], currentScreenshot: null, pendingConfirmation: null }),
}));

