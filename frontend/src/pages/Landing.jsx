// frontend/src/pages/Landing.jsx
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Landing() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-950 text-white flex flex-col items-center justify-center px-4">
      <div className="text-center max-w-2xl">
        <h1 className="text-5xl font-bold mb-4">
          🛡️ NewsGuard <span className="text-blue-400">AI</span>
        </h1>
        <p className="text-gray-400 text-xl mb-8">
          Detect fake news instantly using machine learning.
          Paste any news article and get a credibility score in seconds.
        </p>

        <div className="flex gap-4 justify-center">
          {user ? (
            <Link
              to="/dashboard"
              className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-lg text-lg font-semibold transition"
            >
              Go to Dashboard →
            </Link>
          ) : (
            <>
              <Link
                to="/register"
                className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-lg text-lg font-semibold transition"
              >
                Get Started Free
              </Link>
              <Link
                to="/login"
                className="border border-gray-600 hover:border-gray-400 px-8 py-3 rounded-lg text-lg transition"
              >
                Login
              </Link>
            </>
          )}
        </div>

        {/* Feature cards */}
        <div className="grid grid-cols-3 gap-4 mt-16">
          {[
            { icon: '🤖', title: 'AI Powered', desc: 'TF-IDF + Logistic Regression trained on 44,000+ articles' },
            { icon: '⚡', title: 'Instant Results', desc: 'Get credibility scores in milliseconds' },
            { icon: '📊', title: 'Confidence Score', desc: 'See how confident the model is in each prediction' },
          ].map((f) => (
            <div key={f.title} className="bg-gray-800 p-6 rounded-xl">
              <div className="text-3xl mb-2">{f.icon}</div>
              <h3 className="font-semibold mb-1">{f.title}</h3>
              <p className="text-gray-400 text-sm">{f.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}