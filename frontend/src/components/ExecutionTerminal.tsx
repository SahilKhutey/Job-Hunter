import React, { useState, useEffect, useRef } from "react";

interface LogEntry {
  id: string;
  agent: string;
  message: string;
  time: string;
  type: "info" | "success" | "warning" | "error";
}

export default function ExecutionTerminal({ logs, onAbort }: { logs: LogEntry[], onAbort: () => void }) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  return (
    <div className="fixed bottom-8 right-8 w-[450px] bg-black/90 backdrop-blur-xl border border-violet-500/20 rounded-2xl shadow-2xl overflow-hidden animate-slide-up z-50">
      <div className="bg-violet-500/10 p-4 border-b border-violet-500/10 flex justify-between items-center">
        <div className="flex items-center gap-2">
           <div className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
           <h3 className="text-[11px] font-bold text-violet-400 uppercase tracking-widest">Autonomous Execution Feed</h3>
        </div>
        <button 
          onClick={onAbort}
          className="text-[10px] font-bold text-red-400 hover:text-red-300 transition-colors uppercase tracking-widest bg-red-500/10 px-2 py-1 rounded-md border border-red-500/20"
        >
          Emergency Abort
        </button>
      </div>

      <div 
        ref={scrollRef}
        className="h-[300px] overflow-y-auto p-4 space-y-2 font-mono text-[11px] scrollbar-hide"
      >
        {logs.length === 0 && (
          <div className="h-full flex items-center justify-center text-neutral-600 italic">
            Waiting for agent initialization...
          </div>
        )}
        {logs.map((log) => (
          <div key={log.id} className="flex gap-3 group">
            <span className="text-neutral-700 shrink-0">{log.time}</span>
            <span className={`font-bold shrink-0 ${
              log.agent === 'VisionAgent' ? 'text-sky-400' :
              log.agent === 'AutomationAgent' ? 'text-violet-400' : 'text-emerald-400'
            }`}>
              [{log.agent}]
            </span>
            <span className={`${
              log.type === 'error' ? 'text-red-400' :
              log.type === 'warning' ? 'text-amber-400' :
              log.type === 'success' ? 'text-emerald-400' : 'text-neutral-400'
            }`}>
              {log.message}
            </span>
          </div>
        ))}
      </div>

      <div className="p-3 bg-violet-500/5 border-t border-violet-500/10 flex justify-between items-center">
         <div className="flex gap-1">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className={`w-1.5 h-1.5 rounded-full ${i <= (logs.length % 5) ? 'bg-violet-500' : 'bg-neutral-800'}`} />
            ))}
         </div>
         <p className="text-[9px] text-neutral-500 font-medium">V3.4 Stealth Engine Active</p>
      </div>
    </div>
  );
}
