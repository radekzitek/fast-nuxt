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

let isRefreshing = false;
let failedQueue = [];

function processQueue (error, token = null) {
  failedQueue.forEach(prom => {
    if (error) {
      prom.reject(error);
    } else {
      prom.resolve(token);
    }
  });
  failedQueue = [];
}

api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const auth = useAuthStore();
      if (!auth.refreshToken) {
        auth.logout();
        return Promise.reject(error);
      }
      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject });
        })
          .then(token => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token;
            return api(originalRequest);
          })
          .catch(err => Promise.reject(err));
      }
      isRefreshing = true;
      try {
        const res = await axios.post(
          'http://localhost:8000/api/v1/users/refresh-token',
          { refresh_token: auth.refreshToken }
        );
        auth.setToken(res.data.access_token);
        auth.setRefreshToken(res.data.refresh_token);
        processQueue(null, res.data.access_token);
        originalRequest.headers['Authorization'] = 'Bearer ' + res.data.access_token;
        return api(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        auth.logout();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }
    return Promise.reject(error);
  }
);

export default api;
