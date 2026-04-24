"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUserStore } from "@/store/useUserStore";

const links = [
  { name: "Dashboard", href: "/", icon: "dashboard" },
  { name: "Job Feed", href: "/jobs", icon: "work_outline" },
  { name: "Studio", href: "/studio", icon: "auto_fix_high" },
  { name: "AI Assistant", href: "/assistant", icon: "smart_toy" },
  { name: "Live Automation", href: "/automation", icon: "monitoring" },
  { name: "Analytics", href: "/analytics", icon: "analytics" },
  { name: "Profile Studio", href: "/profile", icon: "account_box" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { profile, clearProfile } = useUserStore();

  return (
    <aside className="w-60 shrink-0 bg-neutral-950 border-r border-neutral-800/60 flex flex-col h-full py-4 px-3">
      {/* Brand */}
      <div className="px-3 mb-6">
        <div className="flex items-center gap-2.5">
          <div className="w-7 h-7 rounded-lg bg-violet-600 flex items-center justify-center shadow-glow-sm">
            <span className="material-icons-round text-white text-sm">bolt</span>
          </div>
          <span className="font-bold text-sm tracking-tight text-white">AI Job Hunter</span>
        </div>
        <div className="mt-2 flex items-center gap-1.5 px-0.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse-slow" />
          <span className="text-[10px] font-medium text-emerald-400">Hunter AI v2.4 · Active</span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 flex flex-col gap-0.5">
        {links.map((link) => {
          const isActive = link.href === "/" ? pathname === "/" : pathname.startsWith(link.href);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`nav-link ${isActive ? "active" : ""}`}
            >
              <span className="material-icons-round text-[18px]">{link.icon}</span>
              {link.name}
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="mt-auto pt-3 border-t border-neutral-800/60 space-y-2">
        <Link href="/settings" className={`nav-link ${pathname === "/settings" ? "active" : ""}`}>
          <span className="material-icons-round text-[18px]">settings_input_component</span>
          Settings
        </Link>

        {/* Real profile pill */}
        {profile ? (
          <div className="px-3 py-2.5 rounded-xl bg-white/[0.03] border border-neutral-800">
            <div className="flex items-center gap-2">
              <div className="w-6 h-6 rounded-full bg-gradient-to-br from-violet-600 to-indigo-700 flex items-center justify-center text-[10px] font-bold text-white shrink-0">
                {profile.full_name?.charAt(0)?.toUpperCase() ?? "?"}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-xs font-semibold text-white truncate">{profile.full_name}</p>
                <p className="text-[10px] text-neutral-500 truncate">{profile.email}</p>
              </div>
            </div>
            <button
              onClick={clearProfile}
              className="mt-2 text-[10px] text-neutral-700 hover:text-neutral-500 transition-colors w-full text-left"
            >
              Sign out
            </button>
          </div>
        ) : (
          <Link href="/onboarding" className="px-3 py-2.5 rounded-xl bg-violet-500/10 border border-violet-500/20 text-xs text-violet-400 font-medium text-center block hover:bg-violet-500/20 transition-colors">
            Complete Setup
          </Link>
        )}
      </div>
    </aside>
  );
}
