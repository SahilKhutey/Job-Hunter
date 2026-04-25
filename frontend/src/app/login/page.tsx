"use client";

import { useState } from "react";
import { useAuthStore } from "@/store/authStore";
import { useUserStore } from "@/store/useUserStore";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { LogIn, Mail, Lock, Loader2, Sparkles } from "lucide-react";

export default function LoginPage() {
  const login = useAuthStore((s) => s.login);
  const launchDemo = useAuthStore((s) => s.launchDemo);
  const setProfileId = useUserStore((s) => s.setProfileId);
  const router = useRouter();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await login(email, password);
      // We might need to fetch the profile ID here if the backend returns it
      router.push("/automation");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Invalid credentials. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLaunch = async () => {
    setDemoLoading(true);
    setError("");
    try {
      await launchDemo();
      const user = useAuthStore.getState().user;
      if (user) {
        setProfileId(user.id); // Assuming user ID matches profile ID for demo
      }
      router.push("/"); // Go to main dashboard
    } catch (err: any) {
      const detail = err.response?.data?.detail;
      setError(detail || "Demo service is currently unavailable. Please try again later.");
    } finally {
      setDemoLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Logo/Header */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-violet-600 flex items-center justify-center shadow-glow mb-4">
            <LogIn className="text-white w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-2">Welcome Back</h1>
          <p className="text-neutral-400 text-sm text-center px-4">
            Sign in to manage your autonomous career execution engine.
          </p>
        </div>

        {/* Card */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-3xl p-8 backdrop-blur-xl shadow-2xl">
          <form onSubmit={handleLogin} className="space-y-6">
            {error && (
              <div className="bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-3 rounded-xl">
                {error}
              </div>
            )}

            <div className="space-y-2">
              <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider ml-1">
                Email Address
              </label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Mail className="h-4 w-4 text-neutral-500 group-focus-within:text-violet-500 transition-colors" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-11 pr-4 py-3 bg-neutral-950 border border-neutral-800 rounded-2xl text-sm text-white placeholder-neutral-600 focus:outline-none focus:ring-2 focus:ring-violet-600/20 focus:border-violet-600 transition-all"
                  placeholder="name@example.com"
                />
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider ml-1">
                Password
              </label>
              <div className="relative group">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <Lock className="h-4 w-4 text-neutral-500 group-focus-within:text-violet-500 transition-colors" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-11 pr-4 py-3 bg-neutral-950 border border-neutral-800 rounded-2xl text-sm text-white placeholder-neutral-600 focus:outline-none focus:ring-2 focus:ring-violet-600/20 focus:border-violet-600 transition-all"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex items-center justify-center gap-2 py-4 px-4 bg-violet-600 hover:bg-violet-500 disabled:opacity-50 disabled:hover:bg-violet-600 text-white font-semibold rounded-2xl shadow-glow-sm hover:shadow-glow transition-all active:scale-[0.98]"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <>
                  <LogIn className="w-4 h-4" />
                  <span>Sign In</span>
                </>
              )}
            </button>

            <div className="relative my-8">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-neutral-800"></div>
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-neutral-950 px-2 text-neutral-500">Or continue with</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <button
                type="button"
                onClick={() => window.location.href = "http://localhost:8000/api/v1/auth/oauth/google"}
                className="flex items-center justify-center gap-2 py-3 px-4 bg-neutral-950 border border-neutral-800 hover:border-neutral-700 text-white rounded-2xl transition-all active:scale-[0.95]"
              >
                <img src="https://www.google.com/favicon.ico" className="w-4 h-4" alt="Google" />
                <span className="text-sm font-medium">Google</span>
              </button>
              <button
                type="button"
                onClick={() => window.location.href = "http://localhost:8000/api/v1/auth/oauth/linkedin"}
                className="flex items-center justify-center gap-2 py-3 px-4 bg-neutral-950 border border-neutral-800 hover:border-neutral-700 text-white rounded-2xl transition-all active:scale-[0.95]"
              >
                <img src="https://www.linkedin.com/favicon.ico" className="w-4 h-4" alt="LinkedIn" />
                <span className="text-sm font-medium">LinkedIn</span>
              </button>
            </div>

            <div className="mt-6">
              <button
                type="button"
                onClick={handleDemoLaunch}
                disabled={demoLoading}
                className="w-full flex items-center justify-center gap-2 py-4 px-4 bg-white hover:bg-neutral-200 text-black font-bold rounded-2xl shadow-glow-white hover:shadow-glow-lg transition-all active:scale-[0.98]"
              >
                {demoLoading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  <>
                    <Sparkles className="w-4 h-4 text-violet-600" />
                    <span>Launch Demo Account</span>
                  </>
                )}
              </button>
              <p className="text-[10px] text-neutral-500 text-center mt-2 font-medium uppercase tracking-widest">
                No setup required • Full Access
              </p>
            </div>
          </form>


          <div className="mt-8 text-center">
            <p className="text-sm text-neutral-500">
              Don't have an account?{" "}
              <Link
                href="/register"
                className="text-violet-400 hover:text-violet-300 font-medium transition-colors"
              >
                Create one now
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
