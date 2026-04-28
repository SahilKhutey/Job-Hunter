import React, { useState, useEffect } from "react";
import { startInterviewSession, submitInterviewResponse } from "@/lib/api";

interface Message {
  id: string;
  type: "ai" | "user";
  text: string;
  feedback?: {
    score: number;
    feedback: string;
    suggestion: string;
  };
}

export default function InterviewSimulator({ jobId, profileId }: { jobId: number; profileId: number }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");
  const [questions, setQuestions] = useState<any[]>([]);
  const [currentIdx, setCurrentIdx] = useState(0);

  useEffect(() => {
    initSession();
  }, [jobId]);

  const initSession = async () => {
    setLoading(true);
    try {
      const data = await startInterviewSession(jobId, profileId);
      setQuestions(data.questions);
      
      const firstQ = data.questions[0];
      const qPrefix = firstQ.type === "strategic" ? "[Strategic Question] " : "";
      
      let welcomeMsg = `Welcome! I'm your AI Interviewer. We'll be practicing for this position.`;
      
      // Add risk awareness if available in the job data (we might need to fetch it or pass it)
      // For now, we'll use the question type as a proxy
      if (data.questions.some((q: any) => q.type === "strategic")) {
        welcomeMsg += `\n\n⚠️ NOTE: I've detected high-stakes elements for this role. I will include strategic questions to test your situational resilience.`;
      }

      setMessages([
        {
          id: "m1",
          type: "ai",
          text: `${welcomeMsg}\n\nHere's your first question: \n\n ${qPrefix}${firstQ.question}`
        }
      ]);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMsg: Message = { id: Date.now().toString(), type: "user", text: input };
    setMessages(prev => [...prev, userMsg]);
    const responseText = input;
    setInput("");
    setLoading(true);

    try {
      const currentQuestion = questions[currentIdx].question;
      const feedback = await submitInterviewResponse(currentQuestion, responseText);
      
      // Add AI Feedback bubble
      const feedbackMsg: Message = {
        id: "f" + Date.now(),
        type: "ai",
        text: `Feedback: Score ${feedback.score}/100. \n\n${feedback.feedback}`,
        feedback: feedback
      };

      // Get next question
      const nextIdx = currentIdx + 1;
      if (nextIdx < questions.length) {
        setCurrentIdx(nextIdx);
        const nextQ = questions[nextIdx];
        const qPrefix = nextQ.type === "strategic" ? "[Strategic Question] " : "";
        const nextQMsg: Message = {
          id: "q" + nextIdx,
          type: "ai",
          text: `Next Question: \n\n ${qPrefix}${nextQ.question}`
        };
        setMessages(prev => [...prev, feedbackMsg, nextQMsg]);
      } else {
        setMessages(prev => [...prev, feedbackMsg, { id: "end", type: "ai", text: "Interview simulation complete! Check your analytics for a full breakdown." }]);
      }
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="flex flex-col h-[600px] card overflow-hidden border-violet-500/10">
      <div className="bg-violet-500/5 p-4 border-b border-violet-500/10 flex justify-between items-center">
        <div className="flex items-center gap-2">
           <span className="material-icons-round text-violet-400">psychology</span>
           <h3 className="font-bold text-white">Interview Intelligence Simulator</h3>
        </div>
        <span className="text-[10px] font-bold text-violet-500 bg-violet-500/10 px-2 py-1 rounded-full uppercase tracking-wider">Phase 3 Active</span>
      </div>

      <div className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide">
        {messages.map((m) => (
          <div key={m.id} className={`flex ${m.type === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] p-4 rounded-2xl relative ${
              m.type === "user" 
                ? "bg-violet-600 text-white rounded-tr-none" 
                : "bg-neutral-800 text-neutral-200 rounded-tl-none border border-neutral-700"
            }`}>
              {m.type === "ai" && m.text.includes("Strategic Question") && (
                <div className="absolute -top-2 -right-2 bg-amber-500 text-black rounded-full p-1 shadow-lg flex items-center justify-center animate-bounce">
                  <span className="material-icons-round text-[14px]">gpp_maybe</span>
                </div>
              )}
              <p className="text-sm whitespace-pre-wrap leading-relaxed">{m.text}</p>
              {m.feedback && (
                <div className="mt-4 pt-4 border-t border-white/10 space-y-2">
                   <p className="text-[10px] font-bold text-violet-300 uppercase tracking-widest">Coaching Tip</p>
                   <p className="text-xs italic text-violet-100">{m.feedback.suggestion}</p>
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
             <div className="bg-neutral-800 p-4 rounded-2xl rounded-tl-none border border-neutral-700 animate-pulse flex gap-2">
                <div className="w-2 h-2 bg-neutral-600 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-neutral-600 rounded-full animate-bounce [animation-delay:-.3s]" />
                <div className="w-2 h-2 bg-neutral-600 rounded-full animate-bounce [animation-delay:-.5s]" />
             </div>
          </div>
        )}
      </div>

      <div className="p-4 bg-neutral-900 border-t border-neutral-800">
        <div className="flex gap-3">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Type your response..."
            className="flex-1 bg-neutral-800 border-none rounded-xl px-4 py-3 text-sm text-white focus:ring-1 focus:ring-violet-500 outline-none"
            disabled={loading}
          />
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className="btn-primary w-12 h-12 flex items-center justify-center rounded-xl p-0"
          >
            <span className="material-icons-round">send</span>
          </button>
        </div>
      </div>
    </div>
  );
}
