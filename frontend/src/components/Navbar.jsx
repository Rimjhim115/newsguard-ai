// frontend/src/components/Navbar.jsx
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="bg-gray-900 text-white px-6 py-4 flex justify-between items-center shadow-lg">
      <Link to="/" className="text-xl font-bold text-blue-400">
        🛡️ NewsGuard AI
      </Link>

      <div className="flex gap-4 items-center">
        {user ? (
          <>
            <span className="text-gray-300 text-sm">
              Hello, {user.username}
            </span>
            <Link
              to="/dashboard"
              className="text-gray-300 hover:text-white transition"
            >
              Dashboard
            </Link>
            <Link
              to="/history"
              className="text-gray-300 hover:text-white transition"
            >
              History
            </Link>
            <button
              onClick={handleLogout}
              className="bg-red-600 hover:bg-red-700 px-4 py-1.5 rounded text-sm transition"
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link
              to="/login"
              className="text-gray-300 hover:text-white transition"
            >
              Login
            </Link>
            <Link
              to="/register"
              className="bg-blue-600 hover:bg-blue-700 px-4 py-1.5 rounded text-sm transition"
            >
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}