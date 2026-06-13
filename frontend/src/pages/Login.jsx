// frontend/src/pages/Login.jsx
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { loginUser, getMyProfile } from '../services/api';
import { useAuth } from '../context/AuthContext';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

const handleSubmit = async (e) => {
  e.preventDefault();
  setError('');
  setLoading(true);

  try {
    // Step 1: Login and get token
    const formData = new URLSearchParams();
    formData.append('username', form.email);
    formData.append('password', form.password);

    const tokenRes = await loginUser(formData);
    const token = tokenRes.data.access_token;

    // Step 2: Store token in localStorage FIRST
    localStorage.setItem('token', token);

    // Step 3: Now fetch profile (token is in localStorage,
    // axios interceptor will pick it up automatically)
    const profileRes = await getMyProfile();

    // Step 4: Update context
    login(token, profileRes.data);
    navigate('/dashboard');

  } catch (err) {
    console.error(err);
    setError(err.response?.data?.detail || 'Login failed. Check your credentials.');
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center px-4">
      <div className="bg-gray-900 p-8 rounded-xl w-full max-w-md shadow-xl">
        <h2 className="text-2xl font-bold text-white mb-6 text-center">
          Welcome Back
        </h2>

        {error && (
          <div className="bg-red-900 border border-red-600 text-red-200 px-4 py-3 rounded mb-4 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-gray-400 text-sm block mb-1">Email</label>
            <input
              name="email"
              type="email"
              value={form.email}
              onChange={handleChange}
              required
              className="w-full bg-gray-800 text-white px-4 py-2.5 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none"
              placeholder="you@email.com"
            />
          </div>

          <div>
            <label className="text-gray-400 text-sm block mb-1">Password</label>
            <input
              name="password"
              type="password"
              value={form.password}
              onChange={handleChange}
              required
              className="w-full bg-gray-800 text-white px-4 py-2.5 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none"
              placeholder="••••••••"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-lg font-semibold transition disabled:opacity-50"
          >
            {loading ? 'Logging in...' : 'Login'}
          </button>
        </form>

        <p className="text-gray-500 text-sm text-center mt-4">
          Don't have an account?{' '}
          <Link to="/register" className="text-blue-400 hover:underline">
            Sign Up
          </Link>
        </p>
      </div>
    </div>
  );
}