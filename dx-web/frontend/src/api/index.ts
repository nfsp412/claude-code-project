import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
    }
    return Promise.reject(error);
  }
);

export default api;

// Dashboard API
export const dashboardApi = {
  getMetrics: () => api.get('/dashboard/metrics'),
  getTaskTrend: (days?: number) => api.get('/dashboard/task-trend', { params: { days } }),
  getTaskDistribution: () => api.get('/dashboard/task-distribution'),
  getRecentTasks: (page?: number, size?: number) =>
    api.get('/dashboard/recent-tasks', { params: { page, size } }),
};

// Task API
export const taskApi = {
  getList: (params?: Record<string, unknown>) => api.get('/tasks', { params }),
  getDetail: (id: string) => api.get(`/tasks/${id}`),
  create: (data: Record<string, unknown>) => api.post('/tasks', data),
  update: (id: string, data: Record<string, unknown>) => api.put(`/tasks/${id}`, data),
  delete: (id: string) => api.delete(`/tasks/${id}`),
};

// Health check
export const healthApi = {
  check: () => api.get('/health'),
};
