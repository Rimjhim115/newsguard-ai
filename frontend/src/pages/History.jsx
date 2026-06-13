// frontend/src/pages/History.jsx
import { useState, useEffect } from 'react';
import { getPredictionHistory } from '../services/api';

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPredictionHistory()
      .then(res => setHistory(res.data))
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <p className="text-gray-400">Loading history...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white px-4 py-10">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold mb-2">Prediction History</h1>
        <p className="text-gray-400 mb-8">All your past news analyses.</p>

        {history.length === 0 ? (
          <div className="bg-gray-900 rounded-xl p-8 text-center">
            <p className="text-gray-500">No predictions yet. Go analyze some news!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {history.map((item) => (
              <div key={item.id} className="bg-gray-900 rounded-xl p-5 shadow">
                <div className="flex justify-between items-start mb-2">
                  <span className={`font-bold text-sm px-3 py-1 rounded-full ${
                    item.prediction === 'FAKE'
                      ? 'bg-red-900 text-red-300'
                      : 'bg-green-900 text-green-300'
                  }`}>
                    {item.prediction === 'FAKE' ? '🔴 FAKE' : '🟢 REAL'}
                  </span>
                  <span className="text-gray-500 text-xs">
                    {new Date(item.created_at + 'Z').toLocaleString('en-IN')}
                  </span>
                </div>
                <p className="text-gray-300 text-sm mt-2">
                  {item.news_text.length > 150
                    ? item.news_text.substring(0, 150) + '...'
                    : item.news_text}
                </p>
                <p className="text-gray-500 text-xs mt-2">
                  Confidence: {Math.round(item.confidence * 100)}%
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}