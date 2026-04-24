"use client";

import { useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { setAccessToken } from "@/lib/auth";
import { useAuthStore } from "@/store/authStore";
import { Loader2 } from "lucide-react";

function OAuthSuccessContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const fetchUser = useAuthStore((s) => s.fetchUser);

  useEffect(() => {
    const access = searchParams.get("access");
    const refresh = searchParams.get("refresh");

    if (access && refresh) {
      setAccessToken(access);
      localStorage.setItem("refresh_token", refresh);
      
      // Bootstrap the user data into the store
      fetchUser().then(() => {
        router.push("/automation");
      });
    } else {
      router.push("/login?error=oauth_failed");
    }
  }, [searchParams, router, fetchUser]);

  return (
    <div className="min-h-screen bg-neutral-950 flex flex-col items-center justify-center p-4">
      <div className="w-16 h-16 rounded-2xl bg-violet-600 flex items-center justify-center shadow-glow mb-6 animate-pulse">
        <Loader2 className="text-white w-8 h-8 animate-spin" />
      </div>
      <h1 className="text-xl font-bold text-white mb-2">Authenticating</h1>
      <p className="text-neutral-500 text-sm animate-pulse">Syncing your autonomous profile...</p>
    </div>
  );
}

export default function OAuthSuccessPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <OAuthSuccessContent />
    </Suspense>
  );
}
