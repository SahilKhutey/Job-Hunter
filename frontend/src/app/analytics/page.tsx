"use client";

import { useEffect, useState } from "react";
import { useUserStore } from "@/store/useUserStore";
import { getDashboardStats, DashboardStats } from "@/lib/api";

function Skeleton({ className }: { className?: string }) {
  return <div className={`bg-neutral-800 rounded-xl animate-pulse ${className}`} />;
}

export default function AnalyticsPage() {
  const { profileId } = useUserStore();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (profileId) {
      getDashboardStats(profileId)
        .then(setStats)
        .finally(() => setLoading(false));
    }
  }, [profileId]);


  const total = stats?.total_applications ?? 0;
  const responses = stats?.responses ?? 0;
  const interviews = stats?.interviews ?? 0;
  const offers = stats?.offers ?? 0;
  const totalJobs = stats?.total_jobs_analyzed ?? 0;
  const aiMatches = stats?.ai_matches_above_threshold ?? 0;

  const funnelSteps = [
    { label: "Jobs Analyzed", value: totalJobs, pct: 100, color: "bg-violet-500" },
    { label: "AI Matches", value: aiMatches, pct: totalJobs > 0 ? (aiMatches / totalJobs) * 100 : 0, color: "bg-violet-400" },
    { label: "Applications Sent", value: total, pct: totalJobs > 0 ? (total / totalJobs) * 100 : 0, color: "bg-sky-500" },
    { label: "Responses", value: responses, pct: total > 0 ? (responses / total) * 100 : 0, color: "bg-emerald-500" },
    { label: "Interviews", value: interviews, pct: total > 0 ? (interviews / total) * 100 : 0, color: "bg-amber-500" },
    { label: "Offers", value: offers, pct: total > 0 ? (offers / total) * 100 : 0, color: "bg-orange-500" },
  ];

  const statusBreakdown = stats?.status_breakdown ?? {};
  const statusColors: Record<string, string> = {
    pending: "bg-neutral-600",
    applied: "bg-violet-500",
    interview: "bg-sky-500",
    offer: "bg-emerald-500",
    rejected: "bg-red-500",
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-fade-in">
      <div>
        <h1 className="text-xl font-bold text-white">Analytics</h1>
        <p className="text-xs text-neutral-500 mt-1">Real-time performance metrics from your job hunt</p>
      </div>

      {/* AI Strategic Insights */}
      {!loading && stats?.ai_insights && stats.ai_insights.length > 0 && (
        <div className="grid grid-cols-3 gap-4">
          {stats.ai_insights.map((insight, idx) => (
            <div 
              key={idx} 
              className={`p-4 rounded-2xl border flex gap-3 items-start animate-slide-up ${
                insight.type === 'warning' ? 'bg-amber-500/5 border-amber-500/20 text-amber-200' :
                insight.type === 'success' ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-200' :
                'bg-sky-500/5 border-sky-500/20 text-sky-200'
              }`}
              style={{ animationDelay: `${idx * 100}ms` }}
            >
              <span className="material-icons-round text-[20px] shrink-0 mt-0.5">
                {insight.type === 'warning' ? 'warning_amber' : 
                 insight.type === 'success' ? 'auto_awesome' : 'info'}
              </span>
              <p className="text-xs font-medium leading-relaxed">{insight.message}</p>
            </div>
          ))}
        </div>
      )}

      {/* Stat Cards */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { label: "Total Applied", value: total, icon: "send", color: "text-violet-400" },
          { label: "Response Rate", value: `${stats?.response_rate ?? 0}%`, icon: "reply", color: "text-sky-400" },
          { label: "Interview Rate", value: `${stats?.interview_rate ?? 0}%`, icon: "event_available", color: "text-emerald-400" },
          { label: "Offers", value: offers || "—", icon: "celebration", color: "text-amber-400" },
        ].map((s, i) => (
          <div key={i} className="stat-card animate-slide-up" style={{ animationDelay: `${i * 60}ms` }}>
            {loading ? (
              <>
                <Skeleton className="w-6 h-6 rounded-lg" />
                <Skeleton className="h-7 w-12 mt-1" />
                <Skeleton className="h-3 w-20" />
              </>
            ) : (
              <>
                <span className={`material-icons-round text-[20px] ${s.color}`}>{s.icon}</span>
                <p className="text-2xl font-bold text-white">{s.value}</p>
                <p className="text-xs text-neutral-500">{s.label}</p>
              </>
            )}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-2 gap-6">
        {/* Funnel */}
        <div className="card p-5">
          <h3 className="font-semibold text-white mb-4">Conversion Funnel</h3>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i}>
                  <Skeleton className="h-3 w-full mb-1.5" />
                  <Skeleton className="h-2 w-full rounded-full" />
                </div>
              ))}
            </div>
          ) : total === 0 && totalJobs === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 text-neutral-700 gap-2">
              <span className="material-icons-round text-3xl">bar_chart</span>
              <p className="text-xs text-center">No data yet — submit some applications to see your funnel.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {funnelSteps.map((step) => (
                <div key={step.label}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-neutral-400">{step.label}</span>
                    <span className="text-white font-medium">{step.value.toLocaleString()}</span>
                  </div>
                  <div className="w-full bg-neutral-800 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full transition-all duration-700 ${step.color}`}
                      style={{ width: `${Math.max(step.pct, step.value > 0 ? 2 : 0)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Status Breakdown */}
        <div className="card p-5">
          <h3 className="font-semibold text-white mb-4">Application Status Breakdown</h3>
          {loading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <div key={i} className="flex items-center gap-3">
                  <Skeleton className="w-3 h-3 rounded-full" />
                  <Skeleton className="h-3 flex-1" />
                  <Skeleton className="h-4 w-8" />
                </div>
              ))}
            </div>
          ) : total === 0 ? (
            <div className="flex flex-col items-center justify-center py-10 text-neutral-700 gap-2">
              <span className="material-icons-round text-3xl">donut_large</span>
              <p className="text-xs text-center">No applications yet.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {Object.entries(statusBreakdown).map(([status, count]) => (
                <div key={status} className="flex items-center gap-3">
                  <div className={`w-2.5 h-2.5 rounded-full shrink-0 ${statusColors[status] ?? "bg-neutral-600"}`} />
                  <span className="text-sm text-neutral-400 flex-1 capitalize">{status}</span>
                  <span className="text-sm font-bold text-white">{count}</span>
                  <span className="text-xs text-neutral-600 w-10 text-right">
                    {total > 0 ? `${Math.round((count / total) * 100)}%` : "—"}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Empty Call to Action */}
      {!loading && total === 0 && (
        <div className="card p-6 flex items-center gap-5 border-violet-500/20 bg-violet-500/5">
          <span className="material-icons-round text-violet-400 text-[32px]">bolt</span>
          <div className="flex-1">
            <p className="font-semibold text-white">Start your job hunt to see analytics here</p>
            <p className="text-xs text-neutral-500 mt-1">
              Go to the Job Feed, find a role, and hit Apply. Every submission feeds into this dashboard automatically.
            </p>
          </div>
          <a href="/jobs" className="btn-primary flex items-center gap-2 shrink-0">
            <span className="material-icons-round text-[16px]">work_outline</span>
            Browse Jobs
          </a>
        </div>
      )}
    </div>
  );
}
