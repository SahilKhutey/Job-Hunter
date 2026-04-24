"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import useWebSocket from "@/hooks/useWebSocket";
import ResumeEditor from "@/components/editor/ResumeEditor";
import LiveViewer from "@/components/automation/LiveViewer";
import AgentLogs from "@/components/automation/AgentLogs";
import { useUserStore } from "@/store/useUserStore";
import { useEditor } from "@/store/useEditor";
import { applyToJob } from "@/lib/api";

export default function StudioPage() {
  const router = useRouter();
  const { profileId, profile } = useUserStore();
  const { blocks, initializeFromProfile, activeJob } = useEditor();
  const [applying, setApplying] = useState(false);

  // Connect WebSocket globally for this page
  useWebSocket();

  // Initialize editor with profile data if empty
  useEffect(() => {
    if (profile && blocks.length === 0) {
      initializeFromProfile(profile);
    }
  }, [profile, blocks.length]);

  const handleApply = async () => {
    if (!profileId || !activeJob) return;
    setApplying(true);
    try {
      await applyToJob({
        job_id: String(activeJob.id),
        job_url: activeJob.url,
        platform: activeJob.company,
        profile_id: profileId,
      });
      router.push("/automation");
    } catch (e) {
      console.error("Apply failed", e);
    }
    setApplying(false);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] animate-fade-in overflow-hidden">
      {/* Header with Job Context & Apply Button */}
      {activeJob && (
        <div className="card mb-4 px-6 py-3 flex items-center justify-between bg-violet-600/5 border-violet-500/20">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-violet-500/10 flex items-center justify-center">
              <span className="material-icons-round text-violet-400">auto_fix_high</span>
            </div>
            <div>
              <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest">Tailoring for</p>
              <p className="text-sm font-bold text-white">{activeJob.title} <span className="text-neutral-500 font-normal">at {activeJob.company}</span></p>
            </div>
          </div>
          <button 
            onClick={handleApply}
            disabled={applying}
            className="btn-primary px-8 py-2.5 text-xs font-bold uppercase tracking-widest flex items-center gap-2 glow-violet"
          >
            <span className="material-icons-round text-sm">{applying ? "sync" : "bolt"}</span>
            {applying ? "Starting..." : "Submit with AI"}
          </button>
        </div>
      )}

      <div className="flex flex-1 gap-5 overflow-hidden">
        {/* Left: Notion-style Resume Editor */}
        <div className="flex-1 flex flex-col card overflow-hidden">
          <ResumeEditor />
        </div>

        {/* Right: Live Panels (stacked) */}
        <div className="w-80 shrink-0 flex flex-col gap-4">
          <div className="flex-1 overflow-hidden">
            <AgentLogs />
          </div>
          <div className="h-64">
            <LiveViewer />
          </div>
        </div>
      </div>
    </div>
  );
}
