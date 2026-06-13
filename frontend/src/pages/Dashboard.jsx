// frontend/src/pages/Dashboard.jsx
import { useState } from 'react';
import { analyzePrediction } from '../services/api';
import { useAuth } from '../context/AuthContext';
import ConfidenceBar from '../components/ConfidenceBar';

export default function Dashboard() {
  const { user } = useAuth();
  const [newsText, setNewsText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async () => {
    if (!newsText.trim()) return;
    setError('');
    setResult(null);
    setLoading(true);

    try {
      const res = await analyzePrediction(newsText);
      setResult(res.data);
    } catch (err) {
      setError('Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white px-4 py-10">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">
          News Analyzer
        </h1>
        <p className="text-gray-400 mb-8">
          Welcome, {user?.username}. Paste a news article below to check its credibility.
        </p>

        {/* Input area */}
        <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
          <textarea
            value={newsText}
            onChange={(e) => setNewsText(e.target.value)}
            placeholder="Paste news headline or article text here..."
            rows={6}
            className="w-full bg-gray-800 text-white px-4 py-3 rounded-lg border border-gray-700 focus:border-blue-500 focus:outline-none resize-none"
          />

          <button
            onClick={handleAnalyze}
            disabled={loading || !newsText.trim()}
            className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-semibold transition disabled:opacity-50"
          >
            {loading ? '🔍 Analyzing...' : '🔍 Analyze News'}
          </button>

          {error && (
            <p className="text-red-400 text-sm mt-3">{error}</p>
          )}
        </div>

        {/* Result */}
        {result && (
          <div className="bg-gray-900 rounded-xl p-6 mt-6 shadow-lg">
            <h2 className="text-lg font-semibold mb-3 text-gray-300">
              Analysis Result
            </h2>
            <p className="text-gray-400 text-sm mb-4 italic">
              "{result.news_text.length > 100
                ? result.news_text.substring(0, 100) + '...'
                : result.news_text}"
            </p>
            <ConfidenceBar
              prediction={result.prediction}
              confidence={result.confidence}
            />
          </div>
        )}
      </div>
    </div>
  );
}