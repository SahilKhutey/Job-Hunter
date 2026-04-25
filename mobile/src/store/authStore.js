import { create } from 'zustand';
import api from '../lib/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export const useAuthStore = create((set) => ({
  user: null,
  isAuthenticated: false,
  loading: false,
  error: null,

  login: async (email, password) => {
    set({ loading: true, error: null });
    try {
      const res = await api.post('/auth/login', { email, password });
      const { access_token, refresh_token } = res.data;

      await AsyncStorage.setItem('access_token', access_token);
      await AsyncStorage.setItem('refresh_token', refresh_token);

      const userRes = await api.get('/user/me');
      set({ user: userRes.data, isAuthenticated: true, loading: false });
    } catch (err) {
      set({ error: err.response?.data?.detail || 'Login failed', loading: false });
      throw err;
    }
  },

  logout: async () => {
    await AsyncStorage.removeItem('access_token');
    await AsyncStorage.removeItem('refresh_token');
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    const token = await AsyncStorage.getItem('access_token');
    if (!token) return;
    
    try {
      const userRes = await api.get('/user/me');
      set({ user: userRes.data, isAuthenticated: true });
    } catch (err) {
      await AsyncStorage.removeItem('access_token');
    }
  }
}));
