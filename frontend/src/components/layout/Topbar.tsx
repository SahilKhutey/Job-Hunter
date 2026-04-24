"use client";

import { usePathname } from "next/navigation";
import { useUserStore } from "@/store/useUserStore";
import { useRealtime } from "@/store/useRealtime";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

const titles: Record<string, string> = {
  "/": "Dashboard",
  "/jobs": "Job Feed",
  "/studio": "Application Studio",
  "/assistant": "AI Assistant",
  "/automation": "Live Automation",
  "/analytics": "Analytics",
  "/profile": "Profile Studio",
  "/settings": "Settings",
};

export default function Topbar() {
  const pathname = usePathname();
  const router = useRouter();
  const title = titles[pathname] ?? "Dashboard";
  const { wsStatus } = useRealtime();
  const { profile } = useUserStore();
  const [search, setSearch] = useState("");

  const handleSearch = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && search.trim()) {
      router.push(`/jobs?q=${encodeURIComponent(search)}`);
    }
  };

  return (
    <header className="h-14 border-b border-neutral-800/60 flex items-center justify-between px-6 bg-neutral-950 sticky top-0 z-20">
      <div className="flex items-center gap-3">
        <h1 className="text-base font-semibold text-white">{title}</h1>
        {/* Live WS indicator */}
        <div className={`hidden sm:flex items-center gap-1.5 text-[10px] font-medium px-2 py-0.5 rounded-full border ${
          wsStatus === "connected"
            ? "text-emerald-400 border-emerald-500/20 bg-emerald-500/5"
            : wsStatus === "connecting"
            ? "text-amber-400 border-amber-500/20 bg-amber-500/5"
            : "text-neutral-600 border-neutral-800"
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${wsStatus === "connected" ? "bg-emerald-400 animate-pulse-slow" : wsStatus === "connecting" ? "bg-amber-400" : "bg-neutral-700"}`} />
          {wsStatus === "connected" ? "Live" : wsStatus === "connecting" ? "Connecting" : "Offline"}
        </div>
      </div>

      <div className="flex items-center gap-3">
        {/* Search */}
        <div className="relative">
          <span className="material-icons-round absolute left-2.5 top-1/2 -translate-y-1/2 text-neutral-500 text-[16px]">search</span>
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={handleSearch}
            className="bg-neutral-900 border border-neutral-800 pl-8 pr-4 py-1.5 rounded-lg text-sm text-neutral-200 placeholder:text-neutral-600 focus:outline-none focus:border-violet-500/60 w-56 transition-all"
            placeholder="Search jobs..."
          />
        </div>

        {/* Run AI */}
        <Link href="/automation" className="btn-primary flex items-center gap-1.5 shadow-glow-sm text-sm">
          <span className="material-icons-round text-[15px]">bolt</span>
          Run AI
        </Link>

        {/* Notification */}
        <button className="relative w-8 h-8 rounded-lg hover:bg-white/5 flex items-center justify-center transition-colors">
          <span className="material-icons-round text-neutral-400 text-[20px]">notifications</span>
        </button>

        {/* Profile avatar */}
        {profile && (
          <Link href="/profile" className="w-8 h-8 rounded-full bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center text-xs font-bold text-white hover:opacity-80 transition-opacity">
            {profile.full_name?.charAt(0)?.toUpperCase() ?? "?"}
          </Link>
        )}
      </div>
    </header>
  );
}
