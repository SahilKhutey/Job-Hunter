"use client";

import { useEffect, useState } from "react";
import { getApplications, ApplicationData } from "@/lib/api";
import { useUserStore } from "@/store/useUserStore";

// ── Components ────────────────────────────────────────────────────────────────

function StatusBadge({ status }: { status: string }) {
  const styles = {
    applied: "bg-blue-500/10 text-blue-400 border-blue-500/20",
    shortlisted: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
    interview: "bg-violet-500/10 text-violet-400 border-violet-500/20",
    rejected: "bg-red-500/10 text-red-400 border-red-500/20",
    offer: "bg-amber-500/10 text-amber-400 border-amber-500/20",
  }[status] || "bg-neutral-800 text-neutral-400 border-neutral-700";

  return (
    <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider border ${styles}`}>
      {status}
    </span>
  );
}

function ApplicationRow({ app }: { app: ApplicationData }) {
  return (
    <tr className="group border-b border-neutral-900/50 hover:bg-white/[0.02] transition-colors">
      <td className="py-4 pl-4">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center text-xs font-bold text-neutral-500 uppercase">
            {app.job?.company?.charAt(0)}
          </div>
          <div>
            <p className="text-sm font-bold text-white leading-tight group-hover:text-violet-400 transition-colors">
              {app.job?.title}
            </p>
            <p className="text-[11px] text-neutral-500 mt-0.5">{app.job?.company}</p>
          </div>
        </div>
      </td>
      <td className="py-4">
        <StatusBadge status={app.status} />
      </td>
      <td className="py-4">
        <div className="flex items-center gap-1.5">
            <span className="text-xs font-bold text-violet-400">{Math.round(app.applied_match_score * 100)}%</span>
            <div className="w-16 bg-neutral-900 rounded-full h-1">
                <div className="h-full bg-violet-500 rounded-full" style={{ width: `${app.applied_match_score * 100}%` }} />
            </div>
        </div>
      </td>
      <td className="py-4">
        <p className="text-[11px] text-neutral-500 font-mono">
            {new Date(app.applied_at).toLocaleDateString()}
        </p>
      </td>
      <td className="py-4 pr-4 text-right">
        <button className="p-2 rounded-lg bg-neutral-900 border border-neutral-800 text-neutral-600 hover:text-white hover:border-neutral-700 transition-all">
            <span className="material-icons-round text-[18px]">more_vert</span>
        </button>
      </td>
    </tr>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────

export default function ApplicationsPage() {
  const { profileId } = useUserStore();
  const [apps, setApps] = useState<ApplicationData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetch = async () => {
      try {
        const data = await getApplications();
        setApps(data);
      } catch (e) {
        console.error("Failed to fetch applications", e);
      }
      setLoading(false);
    };
    fetch();
  }, []);

  return (
    <div className="flex flex-col h-full animate-fade-in p-4 md:p-2">
      {/* Analytics Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="card p-5 bg-neutral-900/30 border-neutral-800/60 shadow-xl">
            <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest mb-4">Total Submissions</p>
            <div className="flex items-baseline gap-2">
                <span className="text-3xl font-black text-white">{apps.length}</span>
                <span className="text-[10px] text-emerald-500 font-bold">+12% vs last week</span>
            </div>
        </div>
        <div className="card p-5 bg-neutral-900/30 border-neutral-800/60 shadow-xl">
            <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest mb-4">Interview Conversion</p>
            <div className="flex items-baseline gap-2">
                <span className="text-3xl font-black text-violet-400">14.5%</span>
                <span className="text-[10px] text-neutral-600 font-bold">Industry Avg: 8%</span>
            </div>
        </div>
        <div className="card p-5 bg-neutral-900/30 border-neutral-800/60 shadow-xl">
            <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest mb-4">Avg Match Score</p>
            <div className="flex items-baseline gap-2">
                <span className="text-3xl font-black text-white">88%</span>
                <span className="text-[10px] text-emerald-500 font-bold">Optimized</span>
            </div>
        </div>
        <div className="card p-5 bg-neutral-900/30 border-neutral-800/60 shadow-xl">
            <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest mb-4">Pipeline Health</p>
            <div className="flex items-baseline gap-2 text-emerald-400">
                <span className="material-icons-round text-2xl">verified</span>
                <span className="text-lg font-bold uppercase tracking-tighter">Excellent</span>
            </div>
        </div>
      </div>

      {/* History Table */}
      <div className="flex-1 card border-neutral-800/60 overflow-hidden flex flex-col bg-neutral-950/20">
        <div className="p-5 border-b border-neutral-900 bg-white/[0.02] flex items-center justify-between">
            <div className="flex items-center gap-3">
                <span className="material-icons-round text-neutral-500">history</span>
                <h2 className="text-sm font-bold text-white uppercase tracking-widest">Application Pipeline</h2>
            </div>
            <div className="flex items-center gap-4">
                <div className="relative">
                    <span className="material-icons-round absolute left-3 top-1/2 -translate-y-1/2 text-neutral-600 text-[14px]">search</span>
                    <input 
                        placeholder="Filter history..." 
                        className="bg-black border border-neutral-800 rounded-lg pl-9 pr-3 py-1.5 text-xs text-white focus:outline-none focus:border-violet-500/50 w-48"
                    />
                </div>
                <button className="flex items-center gap-2 px-3 py-1.5 bg-neutral-900 border border-neutral-800 rounded-lg text-[10px] font-bold text-neutral-400 hover:text-white transition-all">
                    <span className="material-icons-round text-[14px]">file_download</span>
                    EXPORT
                </button>
            </div>
        </div>

        <div className="flex-1 overflow-y-auto custom-scrollbar">
            <table className="w-full text-left border-collapse">
                <thead className="sticky top-0 bg-neutral-950/90 backdrop-blur-sm z-10">
                    <tr className="border-b border-neutral-900">
                        <th className="py-4 pl-4 text-[10px] font-bold text-neutral-600 uppercase tracking-widest">Position / Company</th>
                        <th className="py-4 text-[10px] font-bold text-neutral-600 uppercase tracking-widest">Status</th>
                        <th className="py-4 text-[10px] font-bold text-neutral-600 uppercase tracking-widest">Initial Match</th>
                        <th className="py-4 text-[10px] font-bold text-neutral-600 uppercase tracking-widest">Applied Date</th>
                        <th className="py-4 pr-4"></th>
                    </tr>
                </thead>
                <tbody>
                    {loading ? (
                        [1, 2, 3, 4, 5].map(i => (
                            <tr key={i} className="border-b border-neutral-900/50">
                                <td className="py-4 pl-4"><div className="h-4 w-48 bg-neutral-900 rounded animate-pulse" /></td>
                                <td className="py-4"><div className="h-5 w-20 bg-neutral-900 rounded-full animate-pulse" /></td>
                                <td className="py-4"><div className="h-1 w-24 bg-neutral-900 rounded-full animate-pulse" /></td>
                                <td className="py-4"><div className="h-3 w-20 bg-neutral-900 rounded animate-pulse" /></td>
                                <td className="py-4 pr-4"></td>
                            </tr>
                        ))
                    ) : apps.length === 0 ? (
                        <tr>
                            <td colSpan={5} className="py-20 text-center">
                                <div className="flex flex-col items-center gap-3 opacity-50">
                                    <span className="material-icons-round text-4xl">folder_off</span>
                                    <p className="text-xs font-bold uppercase tracking-widest">No applications in record</p>
                                </div>
                            </td>
                        </tr>
                    ) : (
                        apps.map(app => (
                            <ApplicationRow key={app.id} app={app} />
                        ))
                    )}
                </tbody>
            </table>
        </div>
      </div>
    </div>
  );
}
