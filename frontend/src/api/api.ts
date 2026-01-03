import axios from 'axios';

// Since you are running FastAPI locally
const API_BASE_URL = '/api'; // Using the Vite Proxy

// Create an axios instance to attach the token automatically
const apiClient = axios.create({
  baseURL: API_BASE_URL,
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => {
  return Promise.reject(error);
});

export const authApi = {
  login: async (formData: FormData) => {
    // FastAPI OAuth2 uses form-data (username/password)
    const { data } = await apiClient.post('/auth/token', formData);
    localStorage.setItem('token', data.access_token);
    return data;
  },
  signup: async (userData: any) => {
    const { data } = await apiClient.post('/auth/signup', userData);
    return data;
  },
  logout: () => {
    localStorage.removeItem('token');
    window.location.reload();
  }
};

export const vaultApi = {
  getGallery: async () => {
    const { data } = await apiClient.get('/images/gallery');
    return data;
  },
  getImageUrl: (path: string | undefined) => {
    if (!path) return '';
    const original = path.split('/').pop();
    return `/api/uploads/${original}`;
  }
};

export interface VaultImage {
  id: number;
  original: string;
  keywords: string[];
  ai_versions: string[]; // These come from our optimized /gallery join
};