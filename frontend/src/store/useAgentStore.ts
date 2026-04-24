import { create } from 'zustand';

interface AgentLog {
  id: string;
  agent: string;
  message: string;
  timestamp: string;
}

interface AgentState {
  logs: AgentLog[];
  status: 'idle' | 'running' | 'completed' | 'error';
  addLog: (log: Omit<AgentLog, 'id' | 'timestamp'>) => void;
  setStatus: (status: 'idle' | 'running' | 'completed' | 'error') => void;
  clearLogs: () => void;
}

export const useAgentStore = create<AgentState>((set) => ({
  logs: [],
  status: 'idle',
  addLog: (log) =>
    set((state) => ({
      logs: [
        ...state.logs,
        {
          ...log,
          id: Math.random().toString(36).substr(2, 9),
          timestamp: new Date().toLocaleTimeString(),
        },
      ],
    })),
  setStatus: (status) => set({ status }),
  clearLogs: () => set({ logs: [], status: 'idle' }),
}));
