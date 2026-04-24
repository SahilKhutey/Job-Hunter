"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "Dashboard", icon: "dashboard", href: "/dashboard" },
  { label: "Jobs", icon: "work", href: "/jobs" },
  { label: "Automation", icon: "rocket_launch", href: "/automation" },
  { label: "Studio", icon: "auto_fix_high", href: "/studio" },
];

export default function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 glass-header border-t border-white/5 md:hidden pb-safe">
      <div className="flex items-center justify-around h-16">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex flex-col items-center justify-center w-full h-full gap-1 transition-colors ${
                isActive ? "text-violet-400" : "text-neutral-500"
              }`}
            >
              <span className={`material-icons-round text-[22px] ${isActive ? "animate-pulse-slow" : ""}`}>
                {item.icon}
              </span>
              <span className="text-[10px] font-bold uppercase tracking-widest">
                {item.label}
              </span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
