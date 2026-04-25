import React, { useState } from "react";

export default function NegotiationCopilot() {
  const [loading, setLoading] = useState(false);
  const [offer, setOffer] = useState({
    base: "120,000",
    equity: "0.1%",
    bonus: "0",
  });
  const [strategy, setStrategy] = useState<any>(null);

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
    </div>
  );
}
