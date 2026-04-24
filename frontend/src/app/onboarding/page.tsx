"use client";

import { useState, useRef } from "react";
import { useRouter } from "next/navigation";
import api from "@/lib/api";
import { useAuthStore } from "@/store/authStore";
import { Upload, FileText, Loader2, Rocket, ArrowRight, ShieldCheck } from "lucide-react";

export default function OnboardingPage() {
  const router = useRouter();
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.size > 10 * 1024 * 1024) {
        setError("File size too large. Max 10MB.");
        return;
      }
      setFile(selectedFile);
      setError("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError("");

    try {
      const formData = new FormData();
      formData.append("file", file);

      // Call the new high-fidelity parser
      const res = await api.post("/onboarding/upload-resume", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Save structured data to local storage for the review step
      localStorage.setItem("suggested_profile", JSON.stringify(res.data.profile));
      router.push("/onboarding/review");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Failed to process resume. Please try again or skip.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-950 flex flex-col items-center justify-center p-6 relative overflow-hidden">
      {/* Abstract Background Elements */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-violet-600/10 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-600/5 blur-[120px] rounded-full" />
      </div>

      <div className="w-full max-w-2xl relative z-10">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-violet-500/10 border border-violet-500/20 text-violet-400 text-[10px] font-bold uppercase tracking-widest mb-4">
            <ShieldCheck className="w-3 h-3" />
            <span>Secure Onboarding</span>
          </div>
          <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">Hydrate Your Skill Graph</h1>
          <p className="text-neutral-400 text-lg max-w-md mx-auto leading-relaxed">
            Upload your resume and let our AI agents architect your professional identity.
          </p>
        </div>

        {/* Upload Zone */}
        <div className="bg-neutral-900/50 border border-neutral-800 rounded-3xl p-10 backdrop-blur-xl shadow-2xl">
          <div 
            onClick={() => !loading && fileInputRef.current?.click()}
            className={`border-2 border-dashed rounded-2xl p-16 flex flex-col items-center gap-6 cursor-pointer transition-all duration-300 group ${
              file ? "border-violet-500/60 bg-violet-500/5" : "border-neutral-800 hover:border-violet-500/40 hover:bg-white/[0.01]"
            } ${loading ? "opacity-50 cursor-wait" : ""}`}
          >
            <div className={`w-20 h-20 rounded-3xl flex items-center justify-center transition-all duration-500 ${
              file ? "bg-violet-600 shadow-glow" : "bg-neutral-800 group-hover:bg-neutral-700"
            }`}>
              {loading ? (
                <Loader2 className="text-white w-8 h-8 animate-spin" />
              ) : file ? (
                <FileText className="text-white w-8 h-8" />
              ) : (
                <Upload className="text-neutral-500 group-hover:text-white w-8 h-8 transition-colors" />
              )}
            </div>
            
            <div className="text-center">
              <p className="text-xl font-bold text-white mb-1">
                {file ? file.name : "Drop your resume here"}
              </p>
              <p className="text-sm text-neutral-500">
                {file ? `${(file.size / 1024).toFixed(0)} KB` : "Supports PDF and DOCX (Max 10MB)"}
              </p>
            </div>

            {file && !loading && (
              <button 
                onClick={(e) => {
                  e.stopPropagation();
                  setFile(null);
                }}
                className="text-xs text-neutral-500 hover:text-white transition-colors"
              >
                Change file
              </button>
            )}
          </div>

          <input 
            ref={fileInputRef}
            type="file" 
            accept=".pdf,.docx" 
            className="hidden" 
            onChange={handleFileChange} 
          />

          {error && (
            <div className="mt-6 bg-red-500/10 border border-red-500/20 text-red-400 text-xs p-4 rounded-xl">
              {error}
            </div>
          )}

          <div className="mt-10 flex flex-col gap-4">
            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className="w-full flex items-center justify-center gap-3 py-5 px-6 bg-violet-600 hover:bg-violet-500 disabled:opacity-50 disabled:hover:bg-violet-600 text-white font-bold rounded-2xl shadow-glow-sm hover:shadow-glow transition-all active:scale-[0.98] text-lg"
            >
              {loading ? (
                <>
                  <Loader2 className="w-6 h-6 animate-spin" />
                  <span>Agent Network Parsing...</span>
                </>
              ) : (
                <>
                  <Rocket className="w-6 h-6" />
                  <span>Initialize Profile</span>
                </>
              )}
            </button>
            
            <button
              onClick={() => router.push("/onboarding/manual")}
              disabled={loading}
              className="w-full py-4 text-neutral-500 hover:text-white text-sm font-medium transition-colors flex items-center justify-center gap-2"
            >
              Skip and build manually <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>

        <p className="text-center text-[10px] text-neutral-700 mt-12 tracking-widest uppercase font-bold">
          Job Hunter OS · Privacy First · Local Intelligence
        </p>
      </div>
    </div>
  );
}
