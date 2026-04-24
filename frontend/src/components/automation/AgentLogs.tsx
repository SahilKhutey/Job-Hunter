"use client";

import { useRealtime } from "@/store/useRealtime";

const agentColors: Record<string, string> = {
  ProfileAgent: "text-sky-400",
  JobAgent: "text-amber-400",
  MatchingAgent: "text-violet-400",
  ResumeAgent: "text-emerald-400",
  ApplicationAgent: "text-pink-400",
  ExecutionAgent: "text-orange-400",
  LearningAgent: "text-cyan-400",
  Orchestrator: "text-indigo-400",
};

const statusDot: Record<string, string> = {
  generating: "bg-violet-400 animate-pulse",
  running: "bg-amber-400 animate-pulse",
  completed: "bg-emerald-400",
  failed: "bg-red-500",
  skipped: "bg-neutral-600",
};

export default function AgentLogs() {
  const { logs, clearAll } = useRealtime();

  return (
    <div className="card flex flex-col h-full overflow-hidden">
      <div className="border-b border-neutral-800 px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="material-icons-round text-neutral-400 text-[18px]">account_tree</span>
          <h2 className="text-sm font-semibold text-white">Agent Activity</h2>
        </div>
        <button
          onClick={clearAll}
          className="text-[11px] text-neutral-600 hover:text-neutral-400 transition-colors"
        >
          Clear
        </button>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-1.5 font-mono text-xs">
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full text-neutral-700 gap-2 font-sans">
            <span className="material-icons-round text-4xl">smart_toy</span>
            <p className="text-sm">Waiting for agents to start...</p>
          </div>
        ) : (
          logs.map((log) => (
            <div key={log.id} className="flex items-start gap-2 animate-fade-in py-1 border-b border-neutral-800/40 last:border-0">
              <span className={`w-1.5 h-1.5 rounded-full mt-1.5 shrink-0 ${statusDot[log.status] ?? "bg-neutral-500"}`} />
              <span className="text-neutral-600 shrink-0">{log.timestamp}</span>
              <span className={`shrink-0 font-semibold ${agentColors[log.agent] ?? "text-neutral-400"}`}>
                [{log.agent}]
              </span>
              <span className="text-neutral-300 break-words">{log.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
