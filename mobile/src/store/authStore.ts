import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
    token: string | null;
    user: any | null;
    setToken: (token: string | null) => void;
    setUser: (user: any | null) => void;
    logout: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    token: null,
    user: null,
    setToken: async (token) => {
        if (token) {
            await AsyncStorage.setItem('access_token', token);
        } else {
            await AsyncStorage.removeItem('access_token');
        }
        set({ token });
    },
    setUser: (user) => set({ user }),
    logout: async () => {
        await AsyncStorage.removeItem('access_token');
        set({ token: null, user: null });
    }
}));
