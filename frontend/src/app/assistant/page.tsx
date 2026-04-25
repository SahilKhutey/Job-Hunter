"use client";

import React, { useState, useEffect } from "react";
import { getJobs, JobData } from "@/lib/api";
import { useUserStore } from "@/store/useUserStore";
import InterviewSimulator from "@/components/features/InterviewSimulator";
import NegotiationCopilot from "@/components/features/NegotiationCopilot";

export default function AssistantPage() {
  const { profileId } = useUserStore();
  const [jobs, setJobs] = useState<JobData[]>([]);
  const [selectedJobId, setSelectedJobId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<"interview" | "negotiation">("interview");

  useEffect(() => {
    if (profileId) {
      getJobs({ profile_id: profileId, limit: 5 }).then(setJobs);
    }
  }, [profileId]);

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-white">Career Assistant</h1>
          <p className="text-sm text-neutral-500 mt-1">AI-driven interview practice and strategic coaching</p>
        </div>
        <div className="flex gap-2">
           <div className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full flex items-center gap-2">
              <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
              <span className="text-[10px] font-bold text-emerald-400 uppercase tracking-widest">Cognitive Engine Online</span>
           </div>
        </div>
      </div>

      {!selectedJobId ? (
        <div className="space-y-6">
          <div className="flex bg-neutral-900/50 p-1 rounded-xl border border-neutral-800 w-fit">
             <button 
                onClick={() => setActiveTab("interview")}
                className={`px-6 py-2 text-xs font-bold rounded-lg transition-all ${activeTab === "interview" ? "bg-violet-600 text-white shadow-lg" : "text-neutral-500 hover:text-neutral-300"}`}
             >
                Interview Simulator
             </button>
             <button 
                onClick={() => setActiveTab("negotiation")}
                className={`px-6 py-2 text-xs font-bold rounded-lg transition-all ${activeTab === "negotiation" ? "bg-amber-600 text-white shadow-lg" : "text-neutral-500 hover:text-neutral-300"}`}
             >
                Negotiation Copilot
             </button>
          </div>

          {activeTab === "interview" ? (
            <div className="grid grid-cols-1 gap-4">
              <h2 className="text-lg font-semibold text-white">Select a job to practice for</h2>
              {jobs.map((job) => (
                <button
                  key={job.id}
                  onClick={() => setSelectedJobId(job.id)}
                  className="card p-6 flex justify-between items-center hover:border-violet-500/50 transition-all group text-left"
                >
                  <div>
                    <h3 className="font-bold text-white group-hover:text-violet-400 transition-colors">{job.title}</h3>
                    <p className="text-xs text-neutral-500">{job.company} • {job.location}</p>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                       <p className="text-[10px] font-bold text-neutral-600 uppercase tracking-widest">Match Score</p>
                       <p className="text-sm font-bold text-white">{Math.round(job.match_score * 100)}%</p>
                    </div>
                    <span className="material-icons-round text-neutral-700 group-hover:text-violet-500 transition-colors">play_circle_filled</span>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <NegotiationCopilot />
          )}

          {activeTab === "interview" && jobs.length === 0 && (
             <div className="card p-12 flex flex-col items-center justify-center text-center gap-4">
                <span className="material-icons-round text-4xl text-neutral-800">work_outline</span>
                <p className="text-sm text-neutral-500">No jobs found. Find and apply to a job first to enable simulator practice.</p>
             </div>
          )}
        </div>
      ) : (
        <div className="space-y-4">
          <button 
            onClick={() => setSelectedJobId(null)}
            className="text-xs text-neutral-500 hover:text-white flex items-center gap-1 transition-colors"
          >
            <span className="material-icons-round text-sm">arrow_back</span>
            Back to Job Selection
          </button>
          {profileId && <InterviewSimulator jobId={selectedJobId} profileId={profileId} />}
        </div>
      )}
    </div>
  );
}
