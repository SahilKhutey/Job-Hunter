"use client";

import { useRealtime } from "@/store/useRealtime";

export default function LiveViewer() {
  const { currentScreenshot, wsStatus } = useRealtime();

  return (
    <div className="flex-1 card flex flex-col overflow-hidden bg-black/40 border-neutral-800/60">
      <div className="border-b border-neutral-800 px-5 py-3 flex items-center justify-between bg-neutral-900/20">
        <div className="flex items-center gap-2">
          <span className="material-icons-round text-violet-400 text-[18px]">visibility</span>
          <p className="text-sm font-semibold text-white">Live Browser View</p>
        </div>
        <div className="flex items-center gap-2">
            <span className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest">Resolution: 720p</span>
            <div className="w-px h-3 bg-neutral-800" />
            <span className="text-[10px] text-emerald-500 font-bold uppercase tracking-widest">Active Stream</span>
        </div>
      </div>

      <div className="flex-1 relative bg-neutral-950 flex items-center justify-center overflow-hidden">
        {currentScreenshot ? (
          <img 
            src={`data:image/jpeg;base64,${currentScreenshot}`} 
            alt="Live Automation"
            className="w-full h-full object-contain animate-fade-in"
          />
        ) : (
          <div className="flex flex-col items-center gap-4 text-neutral-700">
            <div className="relative">
                <div className="absolute inset-0 bg-violet-600/10 blur-xl rounded-full" />
                <span className="material-icons-round text-5xl relative">browser_updated</span>
            </div>
            <div className="text-center">
                <p className="text-sm font-medium text-neutral-500">Waiting for browser initialization...</p>
                <p className="text-[10px] text-neutral-700 mt-1 uppercase tracking-widest">Agent is warming up engine</p>
            </div>
          </div>
        )}

        {/* HUD Overlay */}
        {currentScreenshot && (
            <div className="absolute top-4 right-4 flex flex-col gap-2 pointer-events-none">
                <div className="bg-black/60 backdrop-blur-md border border-white/10 rounded-lg px-3 py-1.5 flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse" />
                    <span className="text-[10px] font-bold text-white uppercase tracking-tighter">REC · LIVE</span>
                </div>
            </div>
        )}

        {/* HITL Confirmation Overlay */}
        {useRealtime((s) => s.pendingConfirmation) && (
            <div className="absolute inset-0 bg-neutral-950/80 backdrop-blur-sm flex items-center justify-center animate-fade-in p-6 z-10">
                <div className="max-w-xs w-full card p-6 bg-neutral-900 border-violet-500/50 shadow-[0_0_30px_rgba(139,92,246,0.2)] text-center space-y-4">
                    <div className="w-12 h-12 rounded-full bg-violet-500/20 flex items-center justify-center mx-auto">
                        <span className="material-icons-round text-violet-400">lock_open</span>
                    </div>
                    <div>
                        <h3 className="text-white font-bold text-lg">Final Review</h3>
                        <p className="text-xs text-neutral-400 mt-1">Agent has filled the form. Please review the live view and confirm to submit.</p>
                    </div>
                    <div className="flex flex-col gap-2 pt-2">
                        <button 
                            onClick={async () => {
                                const jobId = useRealtime.getState().pendingConfirmation;
                                if (!jobId) return;
                                try {
                                    const res = await fetch(`http://localhost:8000/api/v1/execution/confirm/${jobId}`, { method: "POST" });
                                    if (res.ok) {
                                        useRealtime.getState().setPendingConfirmation(null);
                                    }
                                } catch (e) {
                                    console.error("Failed to confirm", e);
                                }
                            }}
                            className="w-full py-3 rounded-xl bg-violet-600 hover:bg-violet-500 text-white text-xs font-bold uppercase tracking-widest transition-all shadow-lg shadow-violet-600/20"
                        >
                            Confirm & Submit
                        </button>
                        <button 
                            onClick={() => useRealtime.getState().setPendingConfirmation(null)}
                            className="w-full py-3 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-400 text-xs font-bold uppercase tracking-widest transition-all"
                        >
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        )}

        {/* Scanline Effect */}
        <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-[length:100%_2px,3px_100%]" />
      </div>

      {/* Bottom Status Bar */}
      <div className="bg-neutral-900/40 border-t border-neutral-800 px-4 py-2 flex items-center justify-between text-[10px]">
        <div className="flex items-center gap-4">
            <span className="text-neutral-500">Engine: <span className="text-neutral-300">Playwright/Chromium</span></span>
            <span className="text-neutral-500">Latency: <span className="text-emerald-500">~120ms</span></span>
        </div>
        <div className="flex items-center gap-2">
            <span className="text-neutral-500">Security:</span>
            <span className="flex items-center gap-1 text-emerald-500">
                <span className="material-icons-round text-[12px]">verified_user</span>
                Sovereign
            </span>
        </div>
      </div>
    </div>
  );
}
