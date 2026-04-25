"use client";

import React, { useState } from "react";
import StepIndicator from "@/components/onboarding/StepIndicator";

export default function OnboardingPage() {
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [profile, setProfile] = useState<any>({
    full_name: "Sahil Khutey",
    job_title: "Senior Full Stack Engineer",
    skills: ["React", "TypeScript", "Python", "FastAPI", "PostgreSQL"],
    location: "San Francisco, CA"
  });

  const steps = ["The Seed", "The Identity", "The Target", "The Handshake"];

  const nextStep = () => {
    setLoading(true);
    setTimeout(() => {
      setStep(s => s + 1);
      setLoading(false);
    }, 800);
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center py-20 px-6">
      <div className="mb-16 text-center animate-fade-in-up">
        <div className="bg-violet-500/10 border border-violet-500/20 px-4 py-1.5 rounded-full inline-block mb-4">
           <span className="text-[10px] font-bold text-violet-400 uppercase tracking-widest">Genesis Protocol v1.0</span>
        </div>
        <h1 className="text-4xl font-bold text-white tracking-tight">Setup Your Career Engine</h1>
        <p className="text-neutral-500 mt-2 text-sm max-w-md mx-auto leading-relaxed">
          Initialize your professional profile to activate HunterOS intelligence and stealth automation.
        </p>
      </div>

      <StepIndicator currentStep={step} steps={steps} />

      <div className="w-full max-w-3xl mt-12">
        {step === 1 && (
          <div className="card p-12 border-violet-500/10 text-center animate-fade-in">
             <div className="w-20 h-20 bg-neutral-900 rounded-3xl mx-auto mb-8 flex items-center justify-center border border-neutral-800">
                <span className="material-icons-round text-3xl text-violet-500">description</span>
             </div>
             <h2 className="text-xl font-bold text-white mb-2">Upload Your Resume</h2>
             <p className="text-neutral-500 text-sm mb-10 max-w-xs mx-auto">
                The AI will extract your experience and skills to build your target persona.
             </p>
             <div className="border-2 border-dashed border-neutral-800 rounded-3xl p-12 hover:border-violet-500/50 transition-all cursor-pointer group">
                <span className="material-icons-round text-4xl text-neutral-700 group-hover:text-violet-400 transition-colors mb-4">cloud_upload</span>
                <p className="text-xs font-bold text-neutral-500 uppercase tracking-widest">Drag & Drop PDF/DOCX</p>
             </div>
             <button onClick={nextStep} className="btn-primary mt-12 w-full py-4 text-sm tracking-widest uppercase font-bold">Initialize Extraction</button>
          </div>
        )}

        {step === 2 && (
          <div className="space-y-6 animate-fade-in">
             <div className="grid grid-cols-2 gap-6">
                <div className="card p-6 border-neutral-800">
                   <label className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-4 block">Identity Details</label>
                   <div className="space-y-4">
                      <div>
                         <p className="text-[9px] text-neutral-600 font-bold uppercase mb-1">Full Name</p>
                         <input type="text" value={profile.full_name} className="w-full bg-black/40 border border-neutral-800 rounded-lg p-2.5 text-sm text-white" />
                      </div>
                      <div>
                         <p className="text-[9px] text-neutral-600 font-bold uppercase mb-1">Current Role</p>
                         <input type="text" value={profile.job_title} className="w-full bg-black/40 border border-neutral-800 rounded-lg p-2.5 text-sm text-white" />
                      </div>
                   </div>
                </div>
                <div className="card p-6 border-emerald-500/10">
                   <label className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-4 block">AI Extracted Skills</label>
                   <div className="flex flex-wrap gap-2">
                      {profile.skills.map((s: string, i: number) => (
                        <div key={i} className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-lg text-[10px] font-bold text-emerald-400 uppercase">{s}</div>
                      ))}
                   </div>
                </div>
             </div>
             <div className="card p-6 border-neutral-800">
                <div className="flex justify-between items-center mb-4">
                   <h3 className="text-sm font-bold text-white">Experience Summary</h3>
                   <div className="flex items-center gap-2">
                      <span className="w-2 h-2 bg-emerald-500 rounded-full" />
                      <span className="text-[9px] font-bold text-emerald-500 uppercase">AI Verified</span>
                   </div>
                </div>
                <p className="text-xs text-neutral-400 leading-relaxed italic">
                   "Senior Engineer with 8+ years experience specializing in building high-scale distributed systems using React and Python. Proven track record of leading teams through 3 successful exits..."
                </p>
             </div>
             <button onClick={nextStep} className="btn-primary w-full py-4 text-sm tracking-widest uppercase font-bold bg-violet-600">Confirm Identity</button>
          </div>
        )}

        {step === 3 && (
          <div className="card p-12 border-violet-500/10 animate-fade-in">
             <div className="text-center mb-10">
                <h2 className="text-xl font-bold text-white mb-2">Define Your Mission</h2>
                <p className="text-neutral-500 text-sm">Where should the agents focus their search?</p>
             </div>
             <div className="space-y-8">
                <div className="grid grid-cols-2 gap-6">
                   <div>
                      <p className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-3">Target Locations</p>
                      <div className="flex flex-wrap gap-2">
                         {["Remote", "San Francisco", "New York"].map((l, i) => (
                           <div key={i} className="bg-neutral-900 px-3 py-2 rounded-xl text-xs text-white border border-neutral-800 flex items-center gap-2">
                              {l} <span className="material-icons-round text-neutral-600 text-[10px] hover:text-red-400 cursor-pointer">close</span>
                           </div>
                         ))}
                      </div>
                   </div>
                   <div>
                      <p className="text-[10px] font-bold text-neutral-500 uppercase tracking-widest mb-3">Salary Floor</p>
                      <div className="relative">
                         <span className="absolute left-4 top-1/2 -translate-y-1/2 text-neutral-600 text-sm">$</span>
                         <input type="text" placeholder="150,000" className="w-full bg-black/40 border border-neutral-800 rounded-xl p-3 pl-8 text-sm text-white" />
                      </div>
                   </div>
                </div>
                <button onClick={nextStep} className="btn-primary w-full py-4 text-sm tracking-widest uppercase font-bold">Lock Strategic Targets</button>
             </div>
          </div>
        )}

        {step === 4 && (
          <div className="card p-12 border-emerald-500/10 text-center animate-fade-in">
             <div className="w-20 h-20 bg-emerald-500/20 rounded-full mx-auto mb-8 flex items-center justify-center">
                <span className="material-icons-round text-4xl text-emerald-500">task_alt</span>
             </div>
             <h2 className="text-xl font-bold text-white mb-2">Engines Online</h2>
             <p className="text-neutral-500 text-sm mb-12">Setup complete. Your autonomous career engine is ready for deployment.</p>
             
             <div className="grid grid-cols-2 gap-6 mb-12">
                <div className="card p-6 border-sky-500/20 bg-sky-500/5 hover:bg-sky-500/10 transition-colors cursor-pointer">
                   <span className="material-icons-round text-sky-400 mb-3">extension</span>
                   <p className="text-[10px] font-bold text-white uppercase tracking-widest">Connect Extension</p>
                </div>
                <div className="card p-6 border-amber-500/20 bg-amber-500/5 hover:bg-amber-500/10 transition-colors cursor-pointer">
                   <span className="material-icons-round text-amber-400 mb-3">smartphone</span>
                   <p className="text-[10px] font-bold text-white uppercase tracking-widest">Setup Mobile App</p>
                </div>
             </div>
             
             <button 
                onClick={() => window.location.href = "/"}
                className="btn-primary w-full py-4 text-sm tracking-widest uppercase font-bold bg-emerald-600 hover:bg-emerald-500"
             >
                Launch Dashboard
             </button>
          </div>
        )}
      </div>
    </div>
  );
}
