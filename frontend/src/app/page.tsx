"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useUserStore } from "@/store/useUserStore";
import {
  getDashboardStats, getDashboardActivity, getTopPicks,
  DashboardStats, ActivityEvent, TopPick
} from "@/lib/api";

// ── Skeleton ──────────────────────────────────────────────────────────────────

function Skeleton({ className }: { className?: string }) {
  return <div className={`bg-neutral-800 rounded-xl animate-pulse ${className}`} />;
}

// ── StatsCard ─────────────────────────────────────────────────────────────────

function StatsCard({ icon, label, value, sub, color = "violet", loading }: {
  icon: string; label: string; value: string | number; sub: string; color?: string; loading?: boolean;
}) {
  const colors: Record<string, string> = {
    violet: "text-violet-400 bg-violet-500/10",
    emerald: "text-emerald-400 bg-emerald-500/10",
    amber: "text-amber-400 bg-amber-500/10",
    sky: "text-sky-400 bg-sky-500/10",
  };
  if (loading) {
    return (
      <div className="stat-card">
        <Skeleton className="w-8 h-8 rounded-lg" />
        <Skeleton className="h-7 w-16 mt-1" />
        <Skeleton className="h-3 w-24" />
        <Skeleton className="h-3 w-20" />
      </div>
    );
  }
  return (
    <div className="stat-card animate-slide-up">
      <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${colors[color]}`}>
        <span className="material-icons-round text-[18px]">{icon}</span>
      </div>
      <p className="text-2xl font-bold">{value}</p>
      <p className="text-xs font-medium text-neutral-400">{label}</p>
      <p className="text-[10px] text-neutral-600">{sub}</p>
    </div>
  );
}

// ── ActivityItem ──────────────────────────────────────────────────────────────

function ActivityItem({ icon, title, desc, time }: ActivityEvent) {
  const since = time
    ? (() => {
        const diff = Date.now() - new Date(time).getTime();
        const mins = Math.floor(diff / 60000);
        if (mins < 1) return "just now";
        if (mins < 60) return `${mins}m ago`;
        const hrs = Math.floor(mins / 60);
        if (hrs < 24) return `${hrs}h ago`;
        return `${Math.floor(hrs / 24)}d ago`;
      })()
    : "";

  return (
    <div className="flex items-start gap-3 py-3 border-b border-neutral-800/60 last:border-0 animate-fade-in">
      <div className="w-7 h-7 rounded-lg bg-white/5 flex items-center justify-center shrink-0 mt-0.5">
        <span className="material-icons-round text-violet-400 text-[15px]">{icon}</span>
      </div>
      <div className="flex-1 min-w-0">
        <p className="text-sm font-medium text-white truncate">{title}</p>
        <p className="text-xs text-neutral-500 truncate">{desc}</p>
      </div>
      <span className="text-[10px] text-neutral-600 shrink-0 pt-0.5">{since}</span>
    </div>
  );
}

// ── PickCard ──────────────────────────────────────────────────────────────────

function PickCard({ id, title, company, location, match_score }: TopPick) {
  return (
    <Link href={`/jobs`}>
      <div className="card p-4 flex items-center justify-between hover:border-violet-500/40 transition-all duration-200 cursor-pointer group">
        <div>
          <p className="font-semibold text-sm text-white group-hover:text-violet-300 transition-colors">{title}</p>
          <p className="text-xs text-neutral-500 mt-0.5">{company} · {location}</p>
        </div>
        <div className="text-right">
          <p className="text-lg font-bold text-violet-400">{Math.round(match_score * 100)}%</p>
          <span className="badge-auto">Auto Ready</span>
        </div>
      </div>
    </Link>
  );
}

// ── Empty States ──────────────────────────────────────────────────────────────

function EmptyActivity() {
  return (
    <div className="flex flex-col items-center justify-center py-10 text-neutral-700 gap-2">
      <span className="material-icons-round text-3xl">history</span>
      <p className="text-xs text-center">No activity yet. <br /> Start a job search to see events here.</p>
    </div>
  );
}

function EmptyPicks() {
  return (
    <div className="flex flex-col items-center justify-center py-8 text-neutral-700 gap-2">
      <span className="material-icons-round text-3xl">work_outline</span>
      <p className="text-xs text-center">No matches yet. <br /> Run the AI to score jobs.</p>
      <Link href="/jobs" className="btn-secondary text-xs py-1.5 mt-1">Browse Job Feed</Link>
    </div>
  );
}

// ── Dashboard ─────────────────────────────────────────────────────────────────

export default function Dashboard() {
  const { profileId, profile } = useUserStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [activity, setActivity] = useState<ActivityEvent[]>([]);
  const [picks, setPicks] = useState<TopPick[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!profileId) return;
    setLoading(true);
    Promise.all([
      getDashboardStats(profileId),
      getDashboardActivity(profileId, 10),
      getTopPicks(profileId, 5),
    ])
      .then(([s, a, p]) => {
        setStats(s);
        setActivity(a);
        setPicks(p);
        setError(null);
      })
      .catch(() => setError("Could not connect to backend. Is the FastAPI server running?"))
      .finally(() => setLoading(false));
  }, [profileId]);

  return (
    <div className="space-y-6 max-w-6xl mx-auto animate-fade-in">
      {/* Greeting & Resume Strength */}
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
        <div>
          <h1 className="text-xl md:text-2xl font-bold text-white tracking-tight">
            Good {new Date().getHours() < 12 ? "morning" : new Date().getHours() < 18 ? "afternoon" : "evening"},{" "}
            <span className="text-violet-400">{profile?.full_name?.split(" ")[0] ?? "Hunter"}</span> 👋
          </h1>
          <p className="text-xs text-neutral-500 mt-1">Sovereign intelligence is monitoring your career pipeline.</p>
        </div>

        {/* Resume Strength Meter */}
        <div className="card px-5 py-3 bg-neutral-900/40 border-neutral-800/60 min-w-[280px]">
            <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest">Resume Optimization</span>
                <span className="text-xs font-bold text-violet-400">{(() => {
                    if (!profile) return 0;
                    let s = 0;
                    if (profile.summary) s += 20;
                    if (profile.skills.length > 5) s += 20;
                    if (profile.experience.length > 0) s += 40;
                    if (profile.education.length > 0) s += 10;
                    if (profile.has_resume) s += 10;
                    return Math.min(s, 100);
                })()}%</span>
            </div>
            <div className="h-1.5 w-full bg-neutral-800 rounded-full overflow-hidden">
                <div 
                    className="h-full bg-gradient-to-r from-violet-600 to-violet-400 transition-all duration-1000" 
                    style={{ width: `${profile ? Math.min((profile.summary ? 20 : 0) + (profile.skills.length > 5 ? 20 : 0) + (profile.experience.length > 0 ? 40 : 0) + (profile.education.length > 0 ? 10 : 0) + (profile.has_resume ? 10 : 0), 100) : 0}%` }} 
                />
            </div>
            <p className="text-[9px] text-neutral-600 mt-2 italic font-medium">
                {profile?.has_resume ? "Profile is AI-ready for high-precision matching." : "Upload a resume to unlock agent capabilities."}
            </p>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-amber-400 text-xs flex items-center gap-2">
          <span className="material-icons-round text-[14px]">warning</span>
          {error}
        </div>
      )}

      {/* Stats Row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 md:gap-4">
        <StatsCard
          loading={loading}
          icon="send" label="Applications" color="violet"
          value={stats?.total_applications ?? 0} sub="Total submitted"
        />
        <StatsCard
          loading={loading}
          icon="mark_email_read" label="Responses" color="emerald"
          value={stats?.responses ?? 0} sub={`${stats?.response_rate ?? 0}% rate`}
        />
        <StatsCard
          loading={loading}
          icon="event_available" label="Interviews" color="sky"
          value={stats?.interviews ?? 0} sub="Scheduled or completed"
        />
        <StatsCard
          loading={loading}
          icon="auto_awesome" label="AI Matches" color="amber"
          value={stats?.ai_matches_above_threshold ?? 0} sub={`Above ${profile?.structured_data?.match_threshold ?? 80}% threshold`}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top Picks */}
        <div className="lg:col-span-2 card p-4 md:p-5">

          <div className="flex items-center justify-between mb-4">
            <h2 className="font-semibold text-white">Top Picks for You</h2>
            <Link href="/jobs" className="text-xs text-violet-400 hover:text-violet-300 transition-colors">
              View all
            </Link>
          </div>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="card p-4">
                  <Skeleton className="h-4 w-48" />
                  <Skeleton className="h-3 w-32 mt-2" />
                </div>
              ))}
            </div>
          ) : picks.length > 0 ? (
            <div className="space-y-3">
              {picks.map((p) => <PickCard key={p.id} {...p} />)}
            </div>
          ) : (
            <EmptyPicks />
          )}
        </div>

        {/* Recent Activity */}
        <div className="card p-5">
          <h2 className="font-semibold text-white mb-2">Recent Activity</h2>
          {loading ? (
            <div className="space-y-3 pt-2">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex gap-3 py-2">
                  <Skeleton className="w-7 h-7 rounded-lg shrink-0" />
                  <div className="flex-1 space-y-1.5">
                    <Skeleton className="h-3 w-3/4" />
                    <Skeleton className="h-2 w-1/2" />
                  </div>
                </div>
              ))}
            </div>
          ) : activity.length > 0 ? (
            <div>
              {activity.slice(0, 6).map((a, i) => (
                <ActivityItem key={i} {...a} />
              ))}
            </div>
          ) : (
            <EmptyActivity />
          )}
        </div>
      </div>
    </div>
  );
}
