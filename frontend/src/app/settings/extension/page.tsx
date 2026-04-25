"use client";

import React, { useState } from "react";
import { createExtensionToken } from "@/lib/api";

export default function ExtensionPage() {
  const [token, setToken] = useState("");
  const [generating, setGenerating] = useState(false);

  const generateToken = async () => {
    setGenerating(true);
    try {
      const res = await createExtensionToken();
      setToken(res.token);
    } catch (err) {
      console.error("Failed to generate token", err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-white">Browser Extension</h1>
          <p className="text-sm text-neutral-500 mt-1">Bring HunterOS intelligence to LinkedIn, Indeed, and more</p>
        </div>
        <div className="bg-sky-500/10 border border-sky-500/20 px-3 py-1 rounded-full flex items-center gap-2">
           <span className="w-2 h-2 bg-sky-500 rounded-full animate-pulse" />
           <span className="text-[10px] font-bold text-sky-400 uppercase tracking-widest">Extension Engine Ready</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-8">
        <div className="space-y-6">
           <div className="card p-8 border-sky-500/10">
              <h3 className="font-bold text-white mb-2">1. Connect Your Account</h3>
              <p className="text-sm text-neutral-400 mb-6 leading-relaxed">
                Generate a unique handshake token to securely link the HunterOS extension to your professional profile.
              </p>
              
              {!token ? (
                <button 
                  onClick={generateToken}
                  disabled={generating}
                  className="btn-primary bg-sky-600 hover:bg-sky-500 w-full py-4 flex items-center justify-center gap-2"
                >
                  {generating ? "Generating..." : <><span className="material-icons-round">vpn_key</span> Generate Handshake Token</>}
                </button>
              ) : (
                <div className="space-y-4">
                   <div className="bg-black/50 p-4 rounded-xl border border-sky-500/30 flex justify-between items-center group">
                      <code className="text-sky-300 font-mono text-sm">{token}</code>
                      <button className="text-sky-500 hover:text-white transition-colors">
                        <span className="material-icons-round text-sm">content_copy</span>
                      </button>
                   </div>
                   <p className="text-[10px] text-amber-400 font-medium italic">Never share this token. It provides full access to your career data.</p>
                </div>
              )}
           </div>

           <div className="card p-8 border-neutral-800">
              <h3 className="font-bold text-white mb-4">2. Installation Guide</h3>
              <div className="space-y-4">
                 {[
                   "Download the extension .zip from the releases page.",
                   "Open Chrome Extensions (chrome://extensions).",
                   "Enable 'Developer Mode' in the top right.",
                   "Click 'Load Unpacked' and select the unzipped folder."
                 ].map((step, i) => (
                   <div key={i} className="flex gap-3 items-start">
                      <span className="w-5 h-5 rounded-full bg-neutral-800 text-[10px] font-bold text-neutral-400 flex items-center justify-center shrink-0 mt-0.5">{i+1}</span>
                      <p className="text-xs text-neutral-400 leading-relaxed">{step}</p>
                   </div>
                 ))}
              </div>
           </div>
        </div>

        <div className="space-y-6">
           <div className="card p-0 overflow-hidden border-sky-500/20 shadow-2xl shadow-sky-500/5">
              <div className="bg-neutral-900 p-3 border-b border-neutral-800 flex items-center gap-2">
                 <div className="flex gap-1.5">
                    <div className="w-2.5 h-2.5 rounded-full bg-red-500/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-amber-500/20" />
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/20" />
                 </div>
                 <div className="bg-neutral-800 h-4 w-40 rounded flex items-center px-2">
                    <div className="h-1 w-20 bg-neutral-700 rounded" />
                 </div>
              </div>
              <div className="bg-neutral-950 h-80 p-6 relative overflow-hidden">
                 {/* Mock LinkedIn Page */}
                 <div className="space-y-4 opacity-20">
                    <div className="h-4 w-48 bg-neutral-800 rounded" />
                    <div className="h-2 w-full bg-neutral-800 rounded" />
                    <div className="h-2 w-3/4 bg-neutral-800 rounded" />
                    <div className="h-40 w-full bg-neutral-900 rounded-xl mt-8" />
                 </div>
                 
                 {/* HunterOS Overlay Preview */}
                 <div className="absolute top-10 right-10 w-48 card p-4 border-sky-500/40 bg-black/80 backdrop-blur-md shadow-2xl animate-bounce-subtle">
                    <div className="flex items-center gap-2 mb-3">
                       <span className="material-icons-round text-sky-400 text-sm">auto_awesome</span>
                       <span className="text-[9px] font-bold text-white uppercase tracking-widest">HunterOS Analysis</span>
                    </div>
                    <div className="space-y-3">
                       <div>
                          <div className="flex justify-between items-end mb-1">
                             <p className="text-[8px] text-neutral-500 font-bold uppercase">Match Score</p>
                             <p className="text-xs font-bold text-emerald-400">92%</p>
                          </div>
                          <div className="h-1 w-full bg-neutral-800 rounded-full overflow-hidden">
                             <div className="h-full bg-emerald-500 w-[92%]" />
                          </div>
                       </div>
                       <div className="flex gap-1 flex-wrap">
                          <div className="bg-sky-500/10 px-1.5 py-0.5 rounded text-[7px] text-sky-400 font-bold uppercase">React</div>
                          <div className="bg-sky-500/10 px-1.5 py-0.5 rounded text-[7px] text-sky-400 font-bold uppercase">Node.js</div>
                       </div>
                       <button className="w-full bg-sky-600 text-[8px] font-bold text-white py-1.5 rounded uppercase tracking-wider mt-2">1-Click Apply</button>
                    </div>
                 </div>
              </div>
              <div className="p-4 bg-neutral-900/50">
                 <p className="text-[10px] text-center text-neutral-500 font-medium uppercase tracking-widest">Real-time Overlay Preview</p>
              </div>
           </div>
        </div>
      </div>
    </div>
  );
}
