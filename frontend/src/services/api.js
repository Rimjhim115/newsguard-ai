// frontend/src/services/api.js
import axios from 'axios';

// In Docker: frontend container talks to backend container
// In development: use localhost:8000
const BASE_URL = import.meta.env.VITE_API_URL || 'https://newsguard-ai-e57p.onrender.com/api/v1';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const registerUser = (data) =>
  api.post('/auth/register', data);

export const loginUser = (data) =>
  api.post('/auth/login', data, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  });

export const analyzePrediction = (newsText) =>
  api.post('/predictions/analyze', { news_text: newsText });

export const getPredictionHistory = () =>
  api.get('/predictions/history');

export const getMyProfile = () =>
  api.get('/users/me');