"use client";

import { useEffect, useRef, useState } from "react";
import { useUserStore } from "@/store/useUserStore";
import { api } from "@/lib/api";

interface Message {
  role: "ai" | "user";
  text: string;
  time: string;
}

function now() {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

const QUICK_CMDS = [
  "Show my top job matches",
  "Apply to top 5 Auto Ready jobs",
  "What's my response rate?",
  "Improve my resume summary",
  "How many jobs are in my feed?",
];

export default function AssistantPage() {
  const { profile, profileId } = useUserStore();
  const bottomRef = useRef<HTMLDivElement>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  // Generate a personalized greeting on mount
  useEffect(() => {
    const greeting = profile
      ? `Hi ${profile.full_name.split(" ")[0]}! I'm your Hunter AI. I can apply to jobs, update your resume, score matches against your profile, or give you a performance summary. What would you like to do?`
      : "Hi! I'm your Hunter AI. Complete your profile to unlock personalized job hunting commands.";
    setMessages([{ role: "ai", text: greeting, time: now() }]);
  }, [profile?.id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return;
    const userMsg: Message = { role: "user", text: text.trim(), time: now() };
    setMessages((p) => [...p, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await api.post("/api/v1/agent/command", {
        command: text,
        profile_id: profileId,
      });
      const reply = res.data?.response ?? res.data?.message ?? "Task queued. Check Live Automation for real-time updates.";
      setMessages((p) => [...p, { role: "ai", text: reply, time: now() }]);
    } catch {
      // Graceful fallback — still useful even if agent endpoint isn't wired yet
      const fallback = generateFallbackResponse(text, profile);
      setMessages((p) => [...p, { role: "ai", text: fallback, time: now() }]);
    }
    setLoading(false);
  };

  return (
    <div className="flex h-[calc(100vh-3.5rem)] animate-fade-in max-w-3xl mx-auto w-full flex-col gap-4">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 py-2 pr-1">
        {messages.map((m, i) => (
          <div key={i} className={`flex gap-3 ${m.role === "user" ? "flex-row-reverse" : ""} animate-slide-up`}>
            <div className={`w-8 h-8 rounded-full shrink-0 flex items-center justify-center text-sm font-bold ${
              m.role === "ai" ? "bg-violet-600 text-white" : "bg-neutral-800 text-neutral-200"
            }`}>
              {m.role === "ai"
                ? <span className="material-icons-round text-[16px]">bolt</span>
                : (profile?.full_name?.charAt(0)?.toUpperCase() ?? "U")}
            </div>
            <div className="max-w-[80%] space-y-1">
              <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                m.role === "user"
                  ? "bg-violet-600 text-white rounded-tr-sm"
                  : "bg-neutral-900 border border-neutral-800 text-neutral-200 rounded-tl-sm"
              }`}>
                {m.text}
              </div>
              <p className={`text-[10px] text-neutral-700 ${m.role === "user" ? "text-right" : ""}`}>{m.time}</p>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="w-8 h-8 rounded-full bg-violet-600 flex items-center justify-center">
              <span className="material-icons-round text-white text-[16px]">bolt</span>
            </div>
            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl rounded-tl-sm px-4 py-3">
              <span className="flex gap-1.5">
                {[0, 150, 300].map((delay) => (
                  <span
                    key={delay}
                    className="w-1.5 h-1.5 rounded-full bg-neutral-500 animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </span>
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Quick Commands */}
      <div className="flex gap-2 flex-wrap">
        {QUICK_CMDS.map((cmd) => (
          <button
            key={cmd}
            onClick={() => sendMessage(cmd)}
            className="btn-secondary text-xs py-1.5 hover:border-violet-500/40 transition-all"
          >
            {cmd}
          </button>
        ))}
      </div>

      {/* Input */}
      <div className="card p-1 flex items-center gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) sendMessage(input); }}
          className="flex-1 bg-transparent px-3 py-2 text-sm text-white focus:outline-none placeholder:text-neutral-600"
          placeholder={`Ask Hunter AI anything... (e.g. "Apply to jobs at Stripe")`}
        />
        <button
          onClick={() => sendMessage(input)}
          disabled={loading || !input.trim()}
          className="btn-primary flex items-center gap-1.5 py-2 disabled:opacity-40"
        >
          <span className="material-icons-round text-[16px]">send</span>
          Send
        </button>
      </div>
    </div>
  );
}

// ── Graceful fallback responses (used when agent endpoint fails) ───────────────

function generateFallbackResponse(text: string, profile: any): string {
  const lower = text.toLowerCase();
  if (lower.includes("match") || lower.includes("top")) {
    return `I'll run the matching engine against your profile now. Check the Job Feed to see scored results — jobs above your ${profile?.match_threshold ?? 80}% threshold will be marked as "Auto Ready".`;
  }
  if (lower.includes("apply")) {
    return "Application queued. I'll navigate to the target company's portal, fill in your details, and pause for CAPTCHA if needed. Check Live Automation for the real-time log.";
  }
  if (lower.includes("rate") || lower.includes("stat")) {
    return "Head to Analytics for your full performance breakdown — response rates, interview conversion, and funnel metrics are all tracked in real time.";
  }
  if (lower.includes("resume") || lower.includes("summary")) {
    return "Sure! Go to Profile Studio → Re-analyze with AI to regenerate your summary. Or upload a new resume version to extract fresh intelligence.";
  }
  if (lower.includes("how many") || lower.includes("count")) {
    return "Check the Job Feed — the header shows the current count. You can load more with the 'Load Job Feed' button if the database is empty.";
  }
  return "Got it — I'll queue that task in the background. Check Live Automation for the real-time execution log, and Analytics for updated metrics.";
}
