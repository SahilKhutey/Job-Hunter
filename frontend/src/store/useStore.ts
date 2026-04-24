import { create } from "zustand";

interface Store {
  jobs: any[];
  setJobs: (jobs: any[]) => void;
}

export const useStore = create<Store>((set) => ({
  jobs: [],
  setJobs: (jobs) => set({ jobs }),
}));
