import { useState } from 'react';
import { verifyNews } from '../services/api';
import { useAuth } from '../context/AuthContext';
import VerificationReport from '../components/VerificationReport';

export default function Dashboard() {
  const { user } = useAuth();
  const [newsText, setNewsText] = useState('');
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!newsText.trim()) return;
    setError('');
    setReport(null);
    setLoading(true);

    try {
      const res = await verifyNews(newsText);
      setReport(res.data);
    } catch (err) {
      setError('Verification failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white px-4 py-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">News Verifier</h1>
        <p className="text-gray-400 mb-8">
          Welcome, {user?.username}. Paste a news claim to check its credibility using real-time sources.
        </p>

        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
          <textarea
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste news headline or claim here..."
            rows={5}
            className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none resize-none"
          />

          <button
            onClick={handleAnalyze}
            disabled={loading || !newsText.trim()}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
          >
            {loading ? '🔍 Verifying with live sources...' : '🔍 Verify News'}
          </button>

          {error && <p className="text-red-400 text-sm mt-3">{error}</p>}
        </div>

        {report && <VerificationReport report={report} />}
      </div>
    </div>
  );
}