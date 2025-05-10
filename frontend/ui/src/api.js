import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1',
});

// Add a request interceptor to always include the token
api.interceptors.request.use(
  config => {
    // Try Pinia store first, fallback to localStorage
    let token = null;
    try {
      const auth = useAuthStore();
      token = auth.token;
    } catch {
      token = localStorage.getItem('token');
    }
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => Promise.reject(error)
);

export default api;
