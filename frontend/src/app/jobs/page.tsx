"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useUserStore } from "@/store/useUserStore";
import { useEditor } from "@/store/useEditor";
import { getJobs, applyToJob, JobData } from "@/lib/api";

// ── Helpers ───────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className?: string }) {
  return <div className={`bg-neutral-800 rounded-xl animate-pulse ${className}`} />;
}

function PriorityBadge({ priority }: { priority: string }) {
  if (priority === "HIGH") return <span className="px-2 py-0.5 rounded-full bg-red-500/10 text-red-400 text-[10px] font-bold border border-red-500/20">HIGH PRIORITY</span>;
  if (priority === "MEDIUM") return <span className="px-2 py-0.5 rounded-full bg-violet-500/10 text-violet-400 text-[10px] font-bold border border-violet-500/20">MEDIUM</span>;
  return <span className="px-2 py-0.5 rounded-full bg-neutral-800 text-neutral-500 text-[10px] font-bold border border-neutral-700">LOW</span>;
}

function DifficultyBadge({ difficulty }: { difficulty: number }) {
  const level = difficulty > 0.7 ? "Hard" : difficulty > 0.4 ? "Medium" : "Easy";
  const color = level === "Hard" ? "text-amber-400" : level === "Medium" ? "text-blue-400" : "text-emerald-400";
  return (
    <div className="flex items-center gap-1.5">
        <span className="text-[10px] text-neutral-500 font-bold uppercase">Difficulty:</span>
        <span className={`text-[10px] font-bold ${color}`}>{level}</span>
    </div>
  );
}

function MatchBar({ score }: { score: number }) {
  return (
    <div className="w-full bg-neutral-900 rounded-full h-1 mt-2 overflow-hidden">
      <div
        className="h-full rounded-full bg-gradient-to-r from-violet-600 to-violet-400 transition-all duration-1000 ease-out"
        style={{ width: `${Math.round(score * 100)}%` }}
      />
    </div>
  );
}

function StrategicGuard({ score, flags }: { score: number; flags: string[] }) {
  const isHighRisk = score > 60;
  const colorClass = isHighRisk ? "text-red-400" : "text-emerald-400";
  const bgClass = isHighRisk ? "bg-red-500/10 border-red-500/20" : "bg-emerald-500/10 border-emerald-500/20";

  return (
    <div className={`card p-5 border ${bgClass} transition-all duration-500`}>
      <div className="flex items-center justify-between mb-4">
        <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest">Intelligence Guard</p>
        <span className={`material-icons-round text-[18px] ${colorClass}`}>{isHighRisk ? "gpp_maybe" : "verified_user"}</span>
      </div>
      
      <div className="flex items-baseline gap-2 mb-3">
        <span className={`text-2xl font-black tracking-tighter ${colorClass}`}>{Math.round(score)}%</span>
        <span className="text-[10px] text-neutral-500 font-bold uppercase">Strategic Risk</span>
      </div>

      <div className="space-y-2">
        {flags && flags.length > 0 ? (
          flags.map(f => (
            <div key={f} className="flex items-center gap-2">
              <span className="material-icons-round text-red-500 text-[12px]">report</span>
              <span className="text-[10px] text-red-400 font-bold uppercase tracking-tight">{f}</span>
            </div>
          ))
        ) : (
          <div className="flex items-center gap-2 text-emerald-400/80">
            <span className="material-icons-round text-[12px]">check_circle</span>
            <span className="text-[10px] font-bold uppercase tracking-tight">Verified Safe Origin</span>
          </div>
        )}
      </div>
    </div>
  );
}

// ── Job Card ──────────────────────────────────────────────────────────────────

function JobCard({ job, isActive, onClick }: { job: JobData; isActive: boolean; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className={`card p-4 cursor-pointer transition-all duration-300 hover:border-violet-500/40 group ${
        isActive ? "border-violet-500/60 bg-violet-500/5 shadow-glow-sm" : "border-neutral-800/60"
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="font-bold text-sm text-white truncate group-hover:text-violet-300 transition-colors">{job.title}</p>
          <p className="text-[11px] text-neutral-500 mt-1 font-medium">
            {job.company} · {job.location}
          </p>
        </div>
        <PriorityBadge priority={job.priority} />
      </div>
      
      <div className="mt-4">
        <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold text-violet-400">{Math.round(job.match_score * 100)}% Match</span>
            <DifficultyBadge difficulty={job.difficulty} />
        </div>
        <MatchBar score={job.match_score} />
      </div>

      <div className="flex items-center justify-between mt-4">
        <div className="flex gap-1">
          {job.skills_required.slice(0, 2).map(s => (
            <span key={s} className="text-[9px] text-neutral-400 bg-neutral-800 px-2 py-0.5 rounded-md">{s}</span>
          ))}
          {job.skills_required.length > 2 && <span className="text-[9px] text-neutral-600 self-center">+{job.skills_required.length - 2}</span>}
        </div>
        <button className="text-[10px] font-bold text-neutral-500 hover:text-white transition-colors flex items-center gap-1">
            VIEW DETAILS <span className="material-icons-round text-[14px]">arrow_forward</span>
        </button>
      </div>
    </div>
  );
}

// ── Job Detail ────────────────────────────────────────────────────────────────

function StrategicAdvisor({ job }: { job: JobData }) {
  const isHighRisk = (job.strategic_risk_score || 0) > 60;
  const hasSkillGap = job.skill_gap.length > 0;
  
  // Simulated company health from LearningAgent
  const companyHealth = {
     score: 74,
     recurring_flags: ["Burnout Culture", "Expectation Ambiguity"]
  };

  return (
    <div className="card p-5 bg-violet-600/5 border-violet-500/20 relative overflow-hidden group">
      <div className="absolute top-0 right-0 w-32 h-32 bg-violet-500/5 blur-3xl group-hover:bg-violet-500/10 transition-all duration-700" />
      <p className="text-[10px] text-violet-400 font-bold uppercase mb-4 tracking-widest flex items-center justify-between">
        <span className="flex items-center gap-2">
            <span className="material-icons-round text-[14px] animate-pulse">psychology</span>
            Neural Strategic Advice
        </span>
        <span className="text-[9px] text-neutral-600">CONFIDENCE: 94%</span>
      </p>
      
      <div className="space-y-4 relative z-10">
        {/* Company Health HUD */}
        <div className="mb-6 p-3 bg-white/5 rounded-xl border border-white/5">
           <div className="flex justify-between items-center mb-2">
              <span className="text-[10px] font-bold text-neutral-400 uppercase tracking-tighter">Company Health: {job.company}</span>
              <span className={`text-[10px] font-bold ${companyHealth.score > 80 ? "text-emerald-400" : "text-amber-400"}`}>{companyHealth.score}%</span>
           </div>
           <div className="h-1.5 w-full bg-neutral-800 rounded-full overflow-hidden">
              <div 
                className={`h-full transition-all duration-1000 ${companyHealth.score > 80 ? "bg-emerald-500" : "bg-amber-500"}`} 
                style={{ width: `${companyHealth.score}%` }} 
              />
           </div>
           {companyHealth.recurring_flags.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                 {companyHealth.recurring_flags.map(f => (
                    <span key={f} className="text-[8px] font-black bg-neutral-900 text-neutral-500 px-2 py-0.5 rounded border border-white/5 uppercase">RECURRING: {f}</span>
                 ))}
              </div>
           )}
        </div>

        {isHighRisk && (
          <div className="flex gap-3">
            <div className="w-1.5 h-1.5 rounded-full bg-red-400 mt-1.5 shrink-0" />
            <p className="text-xs text-neutral-300 leading-relaxed">
              <span className="text-red-400 font-bold">Negotiation Priority:</span> High risk signals detected. We recommend a <span className="text-white font-bold">15-20% compensation premium</span> to offset organizational instability.
            </p>
          </div>
        )}
        
        {hasSkillGap && (
          <div className="flex gap-3">
            <div className="w-1.5 h-1.5 rounded-full bg-amber-400 mt-1.5 shrink-0" />
            <p className="text-xs text-neutral-300 leading-relaxed">
              <span className="text-amber-400 font-bold">Studio Optimization:</span> Your profile is missing <span className="text-white font-bold">{job.skill_gap[0]}</span>. Use the Studio to bridge this gap with adjacent transferable experience.
            </p>
          </div>
        )}
        
        {!isHighRisk && !hasSkillGap && (
          <div className="flex gap-3">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 shrink-0" />
            <p className="text-xs text-neutral-300 leading-relaxed">
              <span className="text-emerald-400 font-bold">High-Velocity Signal:</span> Perfect skill parity detected. This is a high-probability match. Recommend immediate <span className="text-white font-bold">Auto-Apply</span> execution.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function JobDetail({ job }: { job: JobData }) {
  const router = useRouter();
  const { profileId } = useUserStore();
  const { setActiveJob } = useEditor();
  const [applying, setApplying] = useState(false);

  const handleApply = async () => {
    if (!profileId) return;
    setApplying(true);
    try {
      await applyToJob({
        job_id: String(job.id),
        job_url: job.url,
        platform: job.company, // Simplified
        profile_id: profileId,
        job_risk_score: job.strategic_risk_score,
        job_red_flags: job.red_flags
      });
      router.push("/automation");
    } catch (e) {
      console.error("Apply failed", e);
    }
    setApplying(false);
  };

  const handleTailor = () => {
    setActiveJob(job);
    router.push("/studio");
  };

  return (
    <div className="h-full flex flex-col animate-fade-in">
      <div className="p-8 border-b border-neutral-900 bg-black/20">
        <div className="flex items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
                <PriorityBadge priority={job.priority} />
                <span className="text-[10px] text-neutral-600 font-bold uppercase tracking-widest">Job ID: #{job.id}</span>
            </div>
            <h2 className="text-2xl font-bold text-white tracking-tight leading-tight">{job.title}</h2>
            <p className="text-neutral-400 font-medium mt-1.5">{job.company} · {job.location}</p>
          </div>
          <div className="text-right">
              <p className="text-[10px] text-neutral-500 font-bold uppercase mb-1">Match Score</p>
              <p className="text-3xl font-black text-violet-400 tracking-tighter">{Math.round(job.match_score * 100)}%</p>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mt-6">
          <span className="px-3 py-1 bg-violet-600/10 border border-violet-500/20 text-violet-300 rounded-full text-[11px] font-bold">
            {job.job_type || "Full-time"}
          </span>
          <span className="px-3 py-1 bg-neutral-900 border border-neutral-800 text-neutral-400 rounded-full text-[11px] font-bold">
            {job.experience_required || "Not specified"}
          </span>
          {job.salary_range && (
            <span className="px-3 py-1 bg-emerald-500/5 border border-emerald-500/10 text-emerald-400 rounded-full text-[11px] font-bold">
              {job.salary_range}
            </span>
          )}
        </div>

        <div className="flex gap-4 mt-8">
          <button 
            onClick={handleApply}
            disabled={applying}
            className="btn-primary flex-1 py-3.5 text-sm flex items-center justify-center gap-2 glow-violet"
          >
            <span className="material-icons-round text-[18px]">{applying ? "sync" : "bolt"}</span>
            {applying ? "Initializing..." : "Initialize Auto-Apply"}
          </button>
          
          <button 
            onClick={handleTailor}
            className="px-6 py-3.5 rounded-xl border border-violet-500/30 bg-violet-500/5 text-violet-400 text-sm font-bold hover:bg-violet-500/10 transition-all flex items-center gap-2"
          >
            <span className="material-icons-round text-[18px]">auto_fix_high</span>
            Tailor Resume
          </button>

          <a href={job.url} target="_blank" rel="noopener noreferrer" className="px-6 py-3.5 rounded-xl border border-neutral-800 bg-neutral-900/50 text-white text-sm font-bold hover:bg-neutral-800 transition-all flex items-center gap-2">
            <span className="material-icons-round text-[18px]">open_in_new</span>
          </a>
        </div>
      </div>

      <div className="p-8 space-y-10 overflow-y-auto flex-1 custom-scrollbar">
        {/* Intelligence Layer */}
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-4 md:gap-6">
            <StrategicAdvisor job={job} />
            <StrategicGuard score={job.strategic_risk_score || 0} flags={job.red_flags || []} />
        </div>

        <div className="grid grid-cols-1 gap-6">
            <div className="card p-5 bg-neutral-900/40 border-neutral-800">
                <p className="text-[10px] text-neutral-500 font-bold uppercase mb-4 tracking-widest">Semantic Alignment</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-6">
                    {/* Matched Skills */}
                    <div className="space-y-2">
                        <p className="text-[9px] font-black text-emerald-500/60 uppercase tracking-tighter mb-2">Verified Strengths</p>
                        <div className="flex flex-wrap gap-2">
                            {job.matched_skills?.map(s => (
                                <span key={s} className="px-2 py-1 bg-emerald-500/5 text-emerald-400 text-[10px] font-bold rounded border border-emerald-500/10 flex items-center gap-1">
                                    <span className="material-icons-round text-[12px]">check_circle</span>
                                    {s}
                                </span>
                            ))}
                        </div>
                    </div>
                    {/* Skill Gap */}
                    <div className="space-y-2">
                        <p className="text-[9px] font-black text-amber-500/60 uppercase tracking-tighter mb-2">Opportunity Gaps</p>
                        <div className="flex flex-wrap gap-2">
                            {job.skill_gap.length > 0 ? (
                                job.skill_gap.map(s => (
                                    <span key={s} className="px-2 py-1 bg-amber-500/5 text-amber-400 text-[10px] font-bold rounded border border-amber-500/10 flex items-center gap-1">
                                        <span className="material-icons-round text-[12px]">warning</span>
                                        {s}
                                    </span>
                                ))
                            ) : (
                                <div className="flex items-center gap-2 text-emerald-400/80 py-1">
                                    <span className="material-icons-round text-[16px]">verified</span>
                                    <span className="text-[10px] font-bold uppercase tracking-tight">Full Skill Parity</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        {/* Description */}
        <div>
          <p className="text-[10px] text-neutral-500 uppercase tracking-widest font-bold mb-4">Job Intelligence Description</p>
          <p className="text-sm text-neutral-400 leading-relaxed whitespace-pre-wrap">{job.description}</p>
        </div>

        {/* Mobile Spacer */}
        <div className="h-28 lg:hidden" />
      </div>

      {/* Floating Action Bar (Mobile) */}
      <div className="fixed bottom-24 left-4 right-4 lg:hidden z-[70]">
        <button 
          onClick={handleApply}
          disabled={applying}
          className="w-full bg-violet-600 hover:bg-violet-500 text-white font-bold py-4 rounded-2xl shadow-2xl shadow-violet-500/40 flex items-center justify-center gap-3 transition-all active:scale-95 border border-violet-400/20"
        >
          {applying ? (
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <>
              <span className="material-icons-round">bolt</span>
              <span>Execute Intelligent Apply</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function JobsPage() {
  const { profileId } = useUserStore();
  const [jobs, setJobs] = useState<JobData[]>([]);
  const [activeJob, setActiveJob] = useState<JobData | null>(null);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [search, setSearch] = useState("");
  const [isDetailOpen, setIsDetailOpen] = useState(false);

  const fetchJobs = async () => {
    setLoading(true);
    try {
      const data = await getJobs({ profile_id: profileId ?? undefined });
      setJobs(data);
    } catch (e) {
      console.error("Failed to fetch jobs", e);
    }
    setLoading(false);
  };

  const handleSeed = async () => {
    setSeeding(true);
    try {
      const { seedJobs } = await import("@/lib/api");
      await seedJobs();
      await fetchJobs();
    } catch (e) {
      console.error("Seed failed", e);
    }
    setSeeding(false);
  };

  useEffect(() => {
    fetchJobs();
  }, [profileId]);

  const displayed = jobs.filter((j) => {
    const q = search.toLowerCase();
    return !q || j.title.toLowerCase().includes(q) || j.company.toLowerCase().includes(q);
  });

  const selectJob = (job: JobData) => {
    setActiveJob(job);
    setIsDetailOpen(true);
  };

  return (
    <div className="flex flex-col md:flex-row h-full md:h-[calc(100vh-3.5rem)] gap-6 animate-fade-in md:p-2">
      {/* Search & Feed Container */}
      <div className={`flex flex-col gap-4 w-full md:w-[420px] shrink-0 ${isDetailOpen && "hidden md:flex"}`}>
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <span className="material-icons-round absolute left-4 top-1/2 -translate-y-1/2 text-neutral-600 text-[18px]">search</span>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search intelligence feed..."
              className="w-full bg-neutral-900 border border-neutral-800 rounded-2xl pl-11 pr-4 py-3 text-sm text-white focus:outline-none focus:border-violet-500/50 transition-all"
            />
          </div>
          <button onClick={fetchJobs} className="p-3 rounded-2xl bg-neutral-900 border border-neutral-800 text-neutral-500 hover:text-white transition-colors">
            <span className="material-icons-round text-[20px]">refresh</span>
          </button>
        </div>

        <div className="flex-1 overflow-y-auto space-y-3 pr-1 custom-scrollbar">
          {loading ? (
            [1, 2, 3].map((i) => (
              <div key={i} className="card p-5 space-y-4">
                <div className="flex justify-between">
                  <div className="space-y-2 flex-1">
                    <Skeleton className="h-4 w-3/4" />
                    <Skeleton className="h-3 w-1/2" />
                  </div>
                  <Skeleton className="h-5 w-20 rounded-full" />
                </div>
                <Skeleton className="h-1 w-full rounded-full" />
              </div>
            ))
          ) : displayed.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-[400px] md:h-full text-center p-8 gap-4">
                <span className="material-icons-round text-neutral-800 text-6xl">radar</span>
                <p className="text-sm text-neutral-600 font-medium">No job intelligence detected.</p>
                <button onClick={handleSeed} disabled={seeding} className="btn-primary px-6 py-2.5 text-xs font-bold uppercase tracking-widest">Initialize Feed</button>
            </div>
          ) : (
            displayed.map((job) => (
              <JobCard
                key={job.id}
                job={job}
                isActive={activeJob?.id === job.id}
                onClick={() => selectJob(job)}
              />
            ))
          )}
        </div>
      </div>

      {/* Right Detail Panel / Mobile Overlay */}
      <div className={`flex-1 flex flex-col fixed inset-0 z-[60] md:relative md:z-0 md:flex bg-black md:bg-transparent ${!isDetailOpen && "hidden"}`}>
        <div className="md:hidden flex items-center justify-between p-4 glass-header">
            <button onClick={() => setIsDetailOpen(false)} className="flex items-center gap-2 text-neutral-400 font-bold text-xs uppercase">
                <span className="material-icons-round">arrow_back</span>
                Back to Feed
            </button>
            <span className="text-[10px] text-violet-400 font-bold uppercase tracking-widest">Job Analysis</span>
        </div>
        
        <div className="flex-1 card overflow-hidden border-neutral-800 md:bg-neutral-950/50">
          {activeJob ? (
            <JobDetail job={activeJob} />
          ) : (
            <div className="hidden md:flex flex-col items-center justify-center h-full text-neutral-700 gap-4">
              <div className="w-16 h-16 rounded-full border border-neutral-900 flex items-center justify-center">
                  <span className="material-icons-round text-3xl">insights</span>
              </div>
              <p className="text-xs font-bold uppercase tracking-widest">Select a listing to analyze</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

