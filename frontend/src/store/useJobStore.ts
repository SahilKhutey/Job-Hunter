import { create } from 'zustand';

interface Job {
  id: number;
  title: string;
  company: string;
  url: string;
  match_score: number;
  ai_decision: string;
  match_analytics?: {
    matched_skills: string[];
    missing_skills: string[];
    alignment_ratio: number;
    recommendation: string;
  };
}

interface JobState {
  jobs: Job[];
  activeJob: Job | null;
  setJobs: (jobs: Job[]) => void;
  setActiveJob: (job: Job) => void;
  updateJobDecision: (id: number, decision: string) => void;
}

export const useJobStore = create<JobState>((set) => ({
  jobs: [],
  activeJob: null,
  setJobs: (jobs) => set({ jobs }),
  setActiveJob: (job) => set({ activeJob: job }),
  updateJobDecision: (id, decision) =>
    set((state) => ({
      jobs: state.jobs.map((j) =>
        j.id === id ? { ...j, ai_decision: decision } : j
      ),
    })),
}));
