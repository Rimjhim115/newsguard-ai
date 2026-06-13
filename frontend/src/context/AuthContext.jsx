// frontend/src/context/AuthContext.jsx
// PURPOSE: Global auth state management.
// Wraps the entire app so any component can access
// the current user and login/logout functions.

import { createContext, useContext, useState, useEffect } from 'react';
import { getMyProfile } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [loading, setLoading] = useState(true);

  // On app load, if token exists, fetch the user profile
  useEffect(() => {
    if (token) {
      getMyProfile()
        .then(res => setUser(res.data))
        .catch(() => {
          // Token is invalid or expired — clear it
          localStorage.removeItem('token');
          setToken(null);
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = (newToken, userData) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook — cleaner than useContext(AuthContext) everywhere
export function useAuth() {
  return useContext(AuthContext);
}