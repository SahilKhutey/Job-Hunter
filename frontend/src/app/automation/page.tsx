"use client";

import { useEffect, useRef } from "react";
import { useUserStore } from "@/store/useUserStore";
import { useRealtime } from "@/store/useRealtime";
import useWebSocket from "@/hooks/useWebSocket";
import LiveViewer from "@/components/automation/LiveViewer";
import { confirmApplication } from "@/lib/api";
import { useState } from "react";

interface LogEntry {
  time: string;
  type: "info" | "success" | "warn" | "error";
  message: string;
  agent?: string;
}

const logColors = {
  info: "text-neutral-400",
  success: "text-emerald-400",
  warn: "text-amber-400",
  error: "text-red-400",
};

const logPrefixes = {
  info: "INF",
  success: "OK ",
  warn: "WRN",
  error: "ERR",
};

function mapAutomationToLogs(automation: any[]): LogEntry[] {
  return automation.map((a) => ({
    time: a.timestamp,
    type: a.status === "done" ? "success" : a.status === "error" ? "error" : "info",
    message: a.step,
    agent: a.agent || "System",
  }));
}

export default function AutomationPage() {
  const { profile } = useUserStore();
  const { automation, wsStatus, clearAll, pendingConfirmation, setPendingConfirmation } = useRealtime();
  const logsEndRef = useRef<HTMLDivElement>(null);
  const [confirming, setConfirming] = useState(false);

  // Connect global WebSocket
  useWebSocket();

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [automation]);

  const logs: LogEntry[] = mapAutomationToLogs(automation);
  const isLive = wsStatus === "connected";

  const handleConfirm = async () => {
    if (!pendingConfirmation) return;
    setConfirming(true);
    try {
      await confirmApplication(pendingConfirmation);
      setPendingConfirmation(null);
    } catch (e) {
      console.error("Confirmation failed", e);
    }
    setConfirming(false);
  };

  return (
    <div className="flex flex-col lg:flex-row h-full lg:h-[calc(100vh-3.5rem)] gap-5 animate-fade-in md:p-2">
      {/* Left/Top: Status Panel & Global Info */}
      <div className="w-full lg:w-80 shrink-0 flex flex-col gap-4 overflow-y-auto lg:pr-1">
        {/* AI Status */}
        <div className="card p-4 bg-neutral-900/40 border-neutral-800/60 shadow-xl">
          <p className="text-[10px] uppercase tracking-widest text-neutral-500 font-bold">Network Status</p>
          <div className="flex items-center gap-3 mt-3">
            <div className={`w-2.5 h-2.5 rounded-full ${
              isLive ? "bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.5)] animate-pulse" : "bg-red-500"
            }`} />
            <div>
              <p className="text-sm font-bold text-white uppercase tracking-tight">
                {isLive ? "Agent Connected" : "Agent Offline"}
              </p>
              <p className="text-[10px] text-neutral-600 font-mono mt-0.5">WS_{wsStatus.toUpperCase()}</p>
            </div>
          </div>
        </div>

        {/* Active Application Stats */}
        <div className="card p-4 md:p-5 space-y-4 md:space-y-5 bg-neutral-900/40 border-neutral-800/60">
          <div className="flex items-center justify-between">
            <p className="text-[10px] uppercase tracking-widest text-neutral-500 font-bold">Application Metrics</p>
            <span className="material-icons-round text-neutral-700 text-sm">analytics</span>
          </div>
          
          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 rounded-xl bg-black/40 border border-neutral-800/50 text-center lg:text-left">
              <p className="text-[10px] text-neutral-600 font-bold uppercase">Success</p>
              <p className="text-lg font-bold text-emerald-400 mt-1">
                {automation.filter(a => a.status === "done").length}
              </p>
            </div>
            <div className="p-3 rounded-xl bg-black/40 border border-neutral-800/50 text-center lg:text-left">
              <p className="text-[10px] text-neutral-600 font-bold uppercase">Errors</p>
              <p className="text-lg font-bold text-red-400 mt-1">
                {automation.filter(a => a.status === "error").length}
              </p>
            </div>
          </div>

          <div className="pt-2 space-y-3">
            <div className="flex justify-between items-center">
                <span className="text-xs text-neutral-500">Pipeline Efficiency</span>
                <span className="text-xs font-bold text-violet-400">94.2%</span>
            </div>
            <div className="h-1 w-full bg-neutral-800 rounded-full overflow-hidden">
                <div className="h-full bg-violet-600 w-[94.2%]" />
            </div>
          </div>
        </div>

        {/* Controls - Hidden on mobile, shown on tablet/desktop or moved to sticky bottom */}
        <div className="hidden lg:flex mt-auto flex-col gap-3">
            <button onClick={clearAll} className="w-full py-3 rounded-xl bg-neutral-900 border border-neutral-800 text-neutral-400 text-xs font-bold uppercase tracking-widest hover:bg-neutral-800 transition-all flex items-center justify-center gap-2">
                <span className="material-icons-round text-sm">delete_sweep</span>
                Clear Terminal
            </button>
            <button className="w-full py-4 rounded-xl bg-red-500/10 border border-red-500/20 text-red-500 text-xs font-bold uppercase tracking-widest hover:bg-red-500/20 transition-all flex items-center justify-center gap-2">
                <span className="material-icons-round text-sm">cancel</span>
                Emergency Abort
            </button>
        </div>
      </div>

      {/* Main Viewport: Live View + Logs */}
      <div className="flex-1 flex flex-col gap-5 overflow-hidden min-h-[500px]">
        {/* Top: Browser Stream */}
        <div className="flex-1 min-h-0">
            <LiveViewer />
        </div>

        {/* Bottom: Event Terminal */}
        <div className="h-64 md:h-72 card flex flex-col overflow-hidden bg-neutral-950/80 border-neutral-800/60 shadow-2xl">
          <div className="border-b border-neutral-800/50 px-5 py-3 flex items-center justify-between bg-black/40">
            <div className="flex items-center gap-2">
              <span className="material-icons-round text-neutral-500 text-[18px]">terminal</span>
              <p className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest">Event Terminal</p>
            </div>
            <div className="flex items-center gap-3">
                <span className="hidden md:inline text-[10px] text-neutral-600 font-mono italic">Listening for agent telemetry...</span>
                <div className="hidden md:block w-px h-3 bg-neutral-800" />
                <span className="text-[10px] text-neutral-500 font-bold">{logs.length} Total</span>
            </div>
          </div>

          <div className="flex-1 overflow-y-auto p-4 md:p-5 font-mono text-[11px] space-y-1 bg-black/20">
            {logs.length === 0 ? (
              <div className="h-full flex flex-col items-center justify-center text-neutral-800 gap-2 opacity-50">
                <span className="material-icons-round text-3xl">hourglass_empty</span>
                <p className="text-[10px] uppercase tracking-widest font-bold">Terminal Idle</p>
              </div>
            ) : (
              logs.map((log, i) => (
                <div key={i} className="flex items-start gap-3 animate-slide-right py-0.5 border-b border-white/[0.02] last:border-0">
                  <span className="text-neutral-700 shrink-0 w-16">{log.time}</span>
                  <span className={`font-bold shrink-0 w-10 ${logColors[log.type]}`}>[{logPrefixes[log.type]}]</span>
                  <span className="text-violet-400/80 shrink-0 min-w-[100px] border-r border-white/5 mr-1">{log.agent?.toUpperCase()}</span>
                  <span className={`flex-1 ${logColors[log.type]} leading-relaxed`}>{log.message}</span>
                </div>
              ))
            )}
            <div ref={logsEndRef} />
          </div>
        </div>
      </div>
      
      {/* Strategic Intervention Modal */}
      {pendingConfirmation && (
        <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="w-full max-w-md card p-8 bg-neutral-950 border-violet-500/40 shadow-[0_0_50px_rgba(139,92,246,0.2)]">
            <div className="flex flex-col items-center text-center">
                <div className="w-20 h-20 rounded-full bg-violet-500/10 border border-violet-500/20 flex items-center justify-center mb-6 animate-pulse">
                    <span className="material-icons-round text-4xl text-violet-400">gpp_maybe</span>
                </div>
                <h3 className="text-xl font-black text-white tracking-tight mb-2">Strategic Intervention Required</h3>
                <p className="text-sm text-neutral-500 leading-relaxed mb-8">
                  The <span className="text-violet-400 font-bold">Execution Agent</span> has reached a critical submission point or detected a high-risk signal. Please review the live browser stream and confirm to proceed.
                </p>
                
                <div className="flex w-full gap-3">
                    <button 
                      onClick={handleConfirm}
                      disabled={confirming}
                      className="flex-1 btn-primary py-4 text-sm font-bold flex items-center justify-center gap-2 glow-violet"
                    >
                        <span className="material-icons-round text-[20px]">{confirming ? "sync" : "verified"}</span>
                        {confirming ? "Processing..." : "Confirm & Submit"}
                    </button>
                    <button 
                      onClick={() => setPendingConfirmation(null)}
                      className="px-6 py-4 rounded-xl border border-neutral-800 bg-neutral-900 text-neutral-400 text-sm font-bold hover:bg-neutral-800 transition-all"
                    >
                        Abort
                    </button>
                </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );

}
