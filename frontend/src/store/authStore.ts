import { create } from "zustand";
import api from "@/lib/api";
import { setAccessToken, logout as authLogout } from "@/lib/auth";

interface User {
  id: number;
  email: string;
  full_name?: string;
  is_active: boolean;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isInitialLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  launchDemo: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isInitialLoading: true,

  login: async (email, password) => {
    const res = await api.post("/auth/login", { email, password });
    const { access_token, refresh_token } = res.data;

    setAccessToken(access_token);
    localStorage.setItem("refresh_token", refresh_token);

    // After login, fetch the user data
    const userRes = await api.get("/user/me");
    set({ user: userRes.data, isAuthenticated: true, isInitialLoading: false });
  },

  register: async (email, password, fullName) => {
    const res = await api.post("/auth/register", { email, password, full_name: fullName });
    const { access_token, refresh_token } = res.data;

    setAccessToken(access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const userRes = await api.get("/user/me");
    set({ user: userRes.data, isAuthenticated: true, isInitialLoading: false });
  },

  logout: () => {
    authLogout();
    set({ user: null, isAuthenticated: false });
  },

  fetchUser: async () => {
    try {
      const refreshToken = localStorage.getItem("refresh_token");
      if (!refreshToken) {
          set({ isInitialLoading: false });
          return;
      }

      // Try to get a fresh access token on boot
      const res = await api.post("/auth/refresh", null, { params: { refresh_token: refreshToken } });
      setAccessToken(res.data.access_token);
      localStorage.setItem("refresh_token", res.data.refresh_token);

      const userRes = await api.get("/user/me");
      set({ user: userRes.data, isAuthenticated: true, isInitialLoading: false });
    } catch (error) {
      authLogout();
      set({ user: null, isAuthenticated: false, isInitialLoading: false });
    }
  },

  launchDemo: async () => {
    const res = await api.post("/auth/demo");
    const { access_token, refresh_token } = res.data;

    setAccessToken(access_token);
    localStorage.setItem("refresh_token", refresh_token);

    const userRes = await api.get("/user/me");
    set({ user: userRes.data, isAuthenticated: true, isInitialLoading: false });
  },
}));
