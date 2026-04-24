"use client";

import { useEffect, useState } from "react";
import { usePathname, useRouter } from "next/navigation";
import { useUserStore } from "@/store/useUserStore";
import { useAuthStore } from "@/store/authStore";
import { useAuth } from "@/hooks/useAuth";
import useWebSocket from "@/hooks/useWebSocket";
import Sidebar from "@/components/layout/Sidebar";
import Topbar from "@/components/layout/Topbar";
import BottomNav from "@/components/layout/BottomNav";

const PUBLIC_PATHS = ["/login", "/register", "/onboarding"];

export default function ClientRoot({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const { isOnboarded, profileId, loadProfile, profile } = useUserStore();
  const { isAuthenticated, isInitialLoading, user } = useAuthStore();
  
  // Bootstrap Auth
  useAuth();

  // Initialize WebSocket (Hook handles internal logic based on auth state)
  useWebSocket();

  const isPublic = PUBLIC_PATHS.some((p) => pathname.startsWith(p));

  useEffect(() => {
    if (isInitialLoading) return;

    // If not authenticated and not on a public path, redirect to login
    if (!isAuthenticated && !isPublic) {
      router.replace("/login");
      return;
    }

    // If authenticated and on login/register, redirect to dashboard/automation
    if (isAuthenticated && (pathname === "/login" || pathname === "/register")) {
        router.replace("/automation");
        return;
    }

    if (isPublic) return;

    if (!isOnboarded || !profileId) {
      router.replace("/onboarding");
      return;
    }

    // Hydrate profile from API if not in memory
    if (!profile && profileId) {
      loadProfile(profileId);
    }
  }, [isAuthenticated, isInitialLoading, isOnboarded, profileId, profile, isPublic, pathname]);

  // Public paths or loading state
  if (isPublic) {
    return <>{children}</>;
  }

  // Show full-screen loading until guard resolves or auth boots
  if (isInitialLoading || (!isAuthenticated && !isPublic)) {
    return (
      <div className="h-screen flex items-center justify-center bg-neutral-950">
        <div className="flex flex-col items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-violet-600 flex items-center justify-center shadow-glow-sm">
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          </div>
          <p className="text-xs text-neutral-500 font-medium tracking-widest uppercase">Initializing Secure Link...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen overflow-hidden bg-black">
      {/* Desktop Sidebar */}
      <div className="hidden md:block">
        <Sidebar />
      </div>

      <div className="flex-1 flex flex-col overflow-hidden relative">
        {/* Responsive Header */}
        <Topbar />
        
        {/* Main Workspace */}
        <main className="flex-1 overflow-y-auto p-4 md:p-6 pb-20 md:pb-6 custom-scrollbar">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>

        {/* Mobile Bottom Nav */}
        <BottomNav />
      </div>
    </div>
  );
}
