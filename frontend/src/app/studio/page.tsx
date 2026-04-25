"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import useWebSocket from "@/hooks/useWebSocket";
import ResumeEditor from "@/components/editor/ResumeEditor";
import LiveViewer from "@/components/automation/LiveViewer";
import AgentLogs from "@/components/automation/AgentLogs";
import { useUserStore } from "@/store/useUserStore";
import { useEditor } from "@/store/useEditor";
import { applyToJob, tailorResume } from "@/lib/api";
import { isDesktop, runLocalAutomation } from "@/lib/desktopBridge";

export default function StudioPage() {
  const router = useRouter();
  const { profileId, profile } = useUserStore();
  const { blocks, initializeFromProfile, activeJob, setVariant, updateBlock } = useEditor();
  const [applying, setApplying] = useState(false);
  const [tailoring, setTailoring] = useState(false);

  // Connect WebSocket globally for this page
  useWebSocket();

  // Initialize editor with profile data if empty
  useEffect(() => {
    if (profile && blocks.length === 0) {
      initializeFromProfile(profile);
    }
  }, [profile, blocks.length]);

  const handleSave = async () => {
    if (!profileId) return;
    const data = exportToProfile();
    try {
      const { updateProfile } = await import("@/lib/api");
      await updateProfile(profileId, data);
    } catch (e) {
      console.error("Save failed", e);
    }
  };

  const handleApply = async () => {
    if (!profileId || !activeJob) return;
    setApplying(true);
    try {
      if (isDesktop()) {
        console.log("Studio: Running local automation mode");
        await runLocalAutomation({
          jobUrl: activeJob.url,
          profileData: profile,
          resumePath: "current", // Place holder or actual path
        });
      } else {
        await applyToJob({
          job_id: String(activeJob.id),
          job_url: activeJob.url,
          platform: activeJob.company,
          profile_id: profileId,
        });
        router.push("/automation");
      }
    } catch (e) {
      console.error("Apply failed", e);
    }
    setApplying(false);
  };

  const handleTailorAI = async () => {
    if (!activeJob) return;
    setTailoring(true);
    try {
      const { tailorResume } = await import("@/lib/api");
      const result = await tailorResume(activeJob.description);
      if (result.status === "success") {
        const variantName = `Tailored: ${activeJob.company}`;
        setVariant(variantName);
        initializeFromTailored(result.resume);
      }
    } catch (e) {
      console.error("Tailoring failed", e);
    }
    setTailoring(false);
  };


  return (
    <div className="flex flex-col h-[calc(100vh-3.5rem)] animate-fade-in overflow-hidden">
      {/* Header with Job Context & Actions */}
      <div className="card mb-4 px-6 py-4 flex items-center justify-between bg-neutral-900/40 border-neutral-800/60 shadow-xl backdrop-blur-md">
        <div className="flex items-center gap-5">
            <button onClick={() => router.back()} className="p-2 rounded-xl bg-neutral-800 hover:bg-neutral-700 text-neutral-400 transition-all">
                <span className="material-icons-round">arrow_back</span>
            </button>
            
            {activeJob ? (
                <div className="flex items-center gap-4 border-l border-neutral-800 pl-5">
                    <div className="w-10 h-10 rounded-xl bg-violet-500/10 flex items-center justify-center">
                        <span className="material-icons-round text-violet-400">auto_fix_high</span>
                    </div>
                    <div>
                        <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest">Tailoring for</p>
                        <p className="text-sm font-bold text-white leading-tight">
                            {activeJob.title} <span className="text-neutral-500 font-normal">at {activeJob.company}</span>
                        </p>
                    </div>
                </div>
            ) : (
                <div className="flex items-center gap-3 border-l border-neutral-800 pl-5">
                    <span className="material-icons-round text-neutral-700">edit_note</span>
                    <p className="text-sm font-bold text-neutral-400 uppercase tracking-widest">Standard Resume Editor</p>
                </div>
            )}
        </div>
        
        <div className="flex items-center gap-3">
            <button 
                onClick={handleSave}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 text-xs font-bold text-neutral-300 transition-all"
            >
                <span className="material-icons-round text-sm">save</span>
                Save
            </button>

            {activeJob && (
                <>
                    <div className="w-px h-6 bg-neutral-800 mx-1" />
                    
                    <button 
                        onClick={handleTailorAI}
                        disabled={tailoring}
                        className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-neutral-800 border border-neutral-700 hover:border-violet-500/50 text-xs font-bold text-white transition-all disabled:opacity-50"
                    >
                        <span className={`material-icons-round text-sm ${tailoring ? "animate-spin" : "text-violet-400"}`}>
                            {tailoring ? "sync" : "auto_fix_high"}
                        </span>
                        {tailoring ? "Analyzing..." : "Tailor with AI"}
                    </button>

                    <button 
                        onClick={handleApply}
                        disabled={applying}
                        className="btn-primary px-8 py-2.5 text-xs font-bold uppercase tracking-widest flex items-center gap-2 glow-violet ml-2"
                    >
                        <span className="material-icons-round text-sm">{applying ? "sync" : "bolt"}</span>
                        {applying ? "Starting..." : "Submit with AI"}
                    </button>
                </>
            )}
        </div>
      </div>


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
