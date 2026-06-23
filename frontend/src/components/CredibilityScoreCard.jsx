export default function CredibilityScoreCard({ report }) {
  const { credibility_score, verdict, explanation, ml_prediction, ml_confidence, sources_found } = report;

  const getVerdictColor = (verdict) => {
    if (verdict === 'CREDIBLE') return 'text-green-400 bg-green-900/30';
    if (verdict === 'POSSIBLY CREDIBLE') return 'text-blue-400 bg-blue-900/30';
    if (verdict === 'QUESTIONABLE') return 'text-yellow-400 bg-yellow-900/30';
    if (verdict === 'NOT CREDIBLE') return 'text-red-400 bg-red-900/30';
    return 'text-gray-400 bg-gray-900/30';
  };

  const getScoreColor = (score) => {
    if (score >= 75) return 'text-green-400';
    if (score >= 50) return 'text-blue-400';
    if (score >= 30) return 'text-yellow-400';
    return 'text-red-400';
  };

  return (
    <div className="bg-gray-900 rounded-xl p-6 shadow-lg">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-xs mb-1">Credibility Score</p>
          <p className={`text-2xl font-bold ${getScoreColor(credibility_score)}`}>
            {credibility_score}<span className="text-sm text-gray-500">/100</span>
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-xs mb-1">Verdict</p>
          <span className={`inline-block text-sm font-semibold px-2 py-1 rounded ${getVerdictColor(verdict)}`}>
            {verdict}
          </span>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-xs mb-1">ML Prediction</p>
          <p className="text-sm font-semibold text-white">
            {ml_prediction} <span className="text-gray-500 font-normal">{ml_confidence}%</span>
          </p>
        </div>

        <div className="bg-gray-800 rounded-lg p-4">
          <p className="text-gray-400 text-xs mb-1">Sources Found</p>
          <p className="text-2xl font-bold text-white">{sources_found}</p>
        </div>
      </div>

      <div className="bg-gray-800 rounded-lg p-4">
        <p className="text-gray-400 text-xs mb-1">ML Prediction</p>
        <p className="text-sm font-semibold text-white">
          {ml_prediction} <span className="text-gray-500 font-normal">{ml_confidence}%</span>
        </p>
        <p className="text-gray-600 text-xs mt-1">
          ⚠️ Limited to training domain
        </p>
      </div>

      <div className="bg-yellow-900/20 border border-yellow-700/40 rounded-lg px-4 py-3">
        <p className="text-yellow-300 text-sm">⚠️ {explanation}</p>
      </div>
    </div>
  );
}