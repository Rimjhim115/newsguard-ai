// frontend/src/components/ConfidenceBar.jsx
// PURPOSE: Visual confidence meter for predictions.

export default function ConfidenceBar({ prediction, confidence }) {
  const percentage = Math.round(confidence * 100);
  const isFake = prediction === 'FAKE';

  return (
    <div className="mt-4">
      <div className="flex justify-between mb-1">
        <span className={`font-bold text-lg ${isFake ? 'text-red-500' : 'text-green-500'}`}>
          {isFake ? '🔴 FAKE NEWS' : '🟢 REAL NEWS'}
        </span>
        <span className="text-gray-300 font-semibold">{percentage}% confident</span>
      </div>

      {/* Progress bar */}
      <div className="w-full bg-gray-700 rounded-full h-4">
        <div
          className={`h-4 rounded-full transition-all duration-500 ${
            isFake ? 'bg-red-500' : 'bg-green-500'
          }`}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {/* Warning for low confidence */}
      {percentage < 70 && (
        <p className="text-yellow-400 text-sm mt-2">
          ⚠️ Low confidence — please verify this news manually.
        </p>
      )}
    </div>
  );
}