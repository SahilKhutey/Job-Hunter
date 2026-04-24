import { create } from "zustand";
import { persist } from "zustand/middleware";
import { ProfileData, getProfile } from "@/lib/api";

interface UserState {
  profileId: number | null;
  profile: ProfileData | null;
  isOnboarded: boolean;
  isLoading: boolean;
  error: string | null;

  setProfileId: (id: number) => void;
  setProfile: (p: ProfileData) => void;
  loadProfile: (id: number) => Promise<void>;
  clearProfile: () => void;
}

export const useUserStore = create<UserState>()(
  persist(
    (set, get) => ({
      profileId: null,
      profile: null,
      isOnboarded: false,
      isLoading: false,
      error: null,

      setProfileId: (id) => set({ profileId: id, isOnboarded: true }),

      setProfile: (profile) =>
        set({ profile, profileId: profile.id, isOnboarded: true, error: null }),

      loadProfile: async (id) => {
        set({ isLoading: true, error: null });
        try {
          const profile = await getProfile(id);
          set({ profile, isLoading: false });
        } catch (e: any) {
          set({
            isLoading: false,
            error: e?.response?.data?.detail ?? "Failed to load profile",
          });
        }
      },

      clearProfile: () =>
        set({ profileId: null, profile: null, isOnboarded: false }),
    }),
    {
      name: "job-hunter-user",
      // Only persist the ID and onboarded flag, not the full profile object
      partialize: (state) => ({
        profileId: state.profileId,
        isOnboarded: state.isOnboarded,
      }),
    }
  )
);
