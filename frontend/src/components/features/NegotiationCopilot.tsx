import React, { useState } from "react";

import { JobData } from "@/lib/api";

export default function NegotiationCopilot({ job }: { job?: JobData }) {
  const [loading, setLoading] = useState(false);
  const [offer, setOffer] = useState({
    base: "120,000",
    equity: "0.1%",
    bonus: "0",
  });
  const [mode, setMode] = useState<"copilot" | "simulator">("copilot");
  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [leverage, setLeverage] = useState(50);

  const handleSendMessage = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput("");
    setLoading(true);
    
    // Simulate API call
    setTimeout(() => {
      setMessages([...newMessages, { 
        role: "assistant", 
        content: "I hear what you're saying about the market rates, but our current offer is already at the high end for this level. We do have some flexibility on equity if that would help close the gap?",
        metrics: { leverage_impact: 65, tone: "yielding" }
      }]);
      setLeverage(65);
      setLoading(false);
    }, 1200);
  };

  const handleGenerate = () => {
    setLoading(true);
    // Simulate API call to negotiation_service
    setTimeout(() => {
      setStrategy({
        grade: 72,
        leverage: [
          "Market average for Senior roles in your region is $145k.",
          "Equity vesting schedule is back-loaded; seek a shorter cliff.",
          "Your specific experience with LLMs justifies a premium."
        ],
        focus: "Prioritize Base Salary and Sign-on Bonus.",
        script: "Dear Hiring Manager,\n\nI appreciate the offer! I'm very excited about the mission. Based on my research and current market rates for my 8 years of experience, I'd like to request a base of $145k and a $10k sign-on bonus..."
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex bg-neutral-900/50 p-1 rounded-xl border border-neutral-800 w-fit">
        <button 
          onClick={() => setMode("copilot")}
          className={`px-4 py-1.5 text-[10px] font-bold rounded-lg transition-all ${mode === "copilot" ? "bg-neutral-800 text-white shadow-lg" : "text-neutral-500"}`}
        >
          Copilot Mode
        </button>
        <button 
          onClick={() => setMode("simulator")}
          className={`px-4 py-1.5 text-[10px] font-bold rounded-lg transition-all ${mode === "simulator" ? "bg-amber-600 text-white shadow-lg" : "text-neutral-500"}`}
        >
          Roleplay Simulator
        </button>
      </div>

      {mode === "copilot" ? (
        <div className="grid grid-cols-3 gap-6">
          <div className="col-span-1 space-y-4">
             <div className="card p-6 border-amber-500/10">
                <h3 className="text-sm font-bold text-white mb-4">Offer Details</h3>
                <div className="space-y-4">
                   <div>
                      <label className="text-[10px] font-bold text-neutral-500 uppercase">Base Salary ($)</label>
                      <input 
                          type="text" 
                          value={offer.base} 
                          onChange={e => setOffer({...offer, base: e.target.value})}
                          className="w-full bg-neutral-900 border border-neutral-800 rounded-lg p-2 text-sm text-white mt-1" 
                      />
                   </div>
                   <div>
                      <label className="text-[10px] font-bold text-neutral-500 uppercase">Equity (%)</label>
                      <input 
                          type="text" 
                          value={offer.equity} 
                          onChange={e => setOffer({...offer, equity: e.target.value})}
                          className="w-full bg-neutral-900 border border-neutral-800 rounded-lg p-2 text-sm text-white mt-1" 
                      />
                   </div>
                   <button 
                      onClick={handleGenerate}
                      disabled={loading}
                      className="btn-primary w-full mt-4 flex items-center justify-center gap-2 bg-amber-600 hover:bg-amber-500"
                   >
                      {loading ? <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <><span className="material-icons-round text-sm">gavel</span> Generate Leverage</>}
                   </button>
                </div>
             </div>
          </div>

          <div className="col-span-2">
             {!strategy ? (
               <div className="h-full card p-8 flex flex-col items-center justify-center text-center border-dashed border-neutral-800">
                  <span className="material-icons-round text-4xl text-neutral-800 mb-4">analytics</span>
                  <p className="text-sm text-neutral-500 max-w-[280px]">Enter your offer details to generate a custom negotiation strategy.</p>
               </div>
             ) : (
               <div className="space-y-4">
                  <div className="flex gap-4">
                     <div className="flex-1 card p-4 border-emerald-500/10">
                        <p className="text-[10px] font-bold text-neutral-500 uppercase">Offer Grade</p>
                        <p className="text-2xl font-bold text-emerald-400">{strategy.grade}/100</p>
                     </div>
                     <div className="flex-[2] card p-4 border-violet-500/10">
                        <p className="text-[10px] font-bold text-neutral-500 uppercase">Strategic Focus</p>
                        <p className="text-xs text-neutral-200 mt-1">{strategy.focus}</p>
                     </div>
                  </div>

                  {job && (job.strategic_risk_score || 0) > 60 && (
                     <div className="card p-4 bg-rose-500/5 border-rose-500/20 flex items-center gap-4 animate-pulse">
                        <div className="w-10 h-10 rounded-full bg-rose-500/10 flex items-center justify-center shrink-0">
                           <span className="material-icons-round text-rose-400">gpp_maybe</span>
                        </div>
                        <div>
                           <p className="text-xs font-black text-rose-400 uppercase tracking-widest">Risk Premium Recommended</p>
                           <p className="text-[10px] text-rose-300/60 leading-tight">This role carries a strategic risk score of {job.strategic_risk_score}. A 15-25% compensation premium is advised to offset potential instability or red flags.</p>
                        </div>
                     </div>
                  )}

                  <div className="card p-6 bg-neutral-900/50">
                     <h4 className="text-xs font-bold text-white mb-3">Key Leverage Points</h4>
                     <div className="space-y-2">
                        {strategy.leverage.map((l: string, i: number) => (
                          <div key={i} className="flex gap-3 items-start">
                             <span className="material-icons-round text-emerald-500 text-sm">check_circle</span>
                             <p className="text-xs text-neutral-400">{l}</p>
                          </div>
                        ))}
                     </div>
                  </div>

                  <div className="card p-6 border-violet-500/20">
                     <div className="flex justify-between items-center mb-4">
                        <h4 className="text-xs font-bold text-white">Negotiation Script</h4>
                        <button className="text-[10px] font-bold text-violet-400 uppercase tracking-widest hover:text-white transition-colors">Copy to Clipboard</button>
                     </div>
                     <div className="bg-black/40 p-4 rounded-xl border border-white/5">
                        <p className="text-xs text-neutral-300 leading-relaxed italic">"{strategy.script}"</p>
                     </div>
                  </div>
               </div>
             )}
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-3 gap-6 h-[500px]">
          <div className="col-span-1 flex flex-col gap-4">
             <div className="card p-6 border-amber-500/10 flex flex-col items-center justify-center">
                <p className="text-[10px] font-black text-amber-500 uppercase tracking-[0.2em] mb-6">Leverage Impact</p>
                <div className="relative w-32 h-32 flex items-center justify-center">
                   <svg className="w-full h-full transform -rotate-90">
                      <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" className="text-neutral-800" />
                      <circle cx="64" cy="64" r="60" stroke="currentColor" strokeWidth="8" fill="transparent" 
                        strokeDasharray={377} strokeDashoffset={377 - (377 * leverage / 100)} 
                        className="text-amber-500 shadow-[0_0_15px_#f59e0b] transition-all duration-1000 ease-out" 
                      />
                   </svg>
                   <div className="absolute flex flex-col items-center">
                      <span className="text-2xl font-black text-white">{leverage}%</span>
                      <span className="text-[8px] font-bold text-neutral-500 uppercase">Power</span>
                   </div>
                </div>
                <p className="text-[10px] text-neutral-400 mt-6 text-center italic">"Your arguments are gaining traction. Keep pushing on the equity front."</p>
             </div>

             <div className="flex-1 card p-4 border-neutral-800 overflow-hidden">
                <p className="text-[10px] font-bold text-neutral-500 uppercase mb-4">Scenario Intelligence</p>
                <div className="space-y-4">
                   <div className="flex gap-2">
                      <span className="material-icons-round text-emerald-400 text-sm">security</span>
                      <p className="text-[10px] text-neutral-400 leading-tight">HM Persona: <span className="text-white">Budget Constrained</span></p>
                   </div>
                   <div className="flex gap-2">
                      <span className="material-icons-round text-amber-400 text-sm">priority_high</span>
                      <p className="text-[10px] text-neutral-400 leading-tight">Stress Test: <span className="text-white">Active</span></p>
                   </div>
                </div>
             </div>
          </div>

          <div className="col-span-2 card flex flex-col overflow-hidden border-neutral-800/60 bg-black/40">
             <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
                {messages.length === 0 ? (
                  <div className="h-full flex flex-col items-center justify-center text-center opacity-30 gap-3">
                     <span className="material-icons-round text-4xl">chat_bubble_outline</span>
                     <p className="text-sm">Initiate roleplay by stating your counter-offer requirements.</p>
                  </div>
                ) : (
                  messages.map((m, i) => (
                    <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}>
                       <div className={`max-w-[80%] p-3 rounded-2xl text-xs leading-relaxed ${
                         m.role === 'user' ? 'bg-violet-600 text-white rounded-tr-none' : 'bg-neutral-800 text-neutral-200 rounded-tl-none'
                       }`}>
                          {m.content}
                       </div>
                    </div>
                  ))
                )}
                {loading && (
                   <div className="flex justify-start animate-fade-in">
                      <div className="bg-neutral-800 p-3 rounded-2xl rounded-tl-none flex gap-1">
                         <div className="w-1.5 h-1.5 bg-neutral-600 rounded-full animate-bounce" />
                         <div className="w-1.5 h-1.5 bg-neutral-600 rounded-full animate-bounce [animation-delay:0.2s]" />
                         <div className="w-1.5 h-1.5 bg-neutral-600 rounded-full animate-bounce [animation-delay:0.4s]" />
                      </div>
                   </div>
                )}
             </div>
             
             <div className="p-4 border-t border-white/5 bg-white/[0.02]">
                <div className="flex gap-2">
                   <input 
                      value={input}
                      onChange={e => setInput(e.target.value)}
                      onKeyDown={e => e.key === 'Enter' && handleSendMessage()}
                      placeholder="Enter your response..."
                      className="flex-1 bg-neutral-900 border border-neutral-800 rounded-xl px-4 py-2 text-xs text-white focus:outline-none focus:border-amber-500/50"
                   />
                   <button 
                      onClick={handleSendMessage}
                      className="p-2 bg-amber-600 hover:bg-amber-500 text-white rounded-xl transition-all"
                   >
                      <span className="material-icons-round text-sm">send</span>
                   </button>
                </div>
             </div>
          </div>
        </div>
      )}
  );
}
