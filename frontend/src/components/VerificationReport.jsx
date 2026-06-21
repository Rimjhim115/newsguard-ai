import CredibilityScoreCard from './CredibilityScoreCard';
import SourceCard from './SourceCard';
import VideoCard from './VideoCard';

export default function VerificationReport({ report }) {
  return (
    <div className="space-y-4 mt-6">
      <CredibilityScoreCard report={report} />

      {report.videos && report.videos.length > 0 && (
        <div>
          <h3 className="text-gray-400 text-sm mb-3">YouTube coverage</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {report.videos.map((video, idx) => (
              <VideoCard key={idx} video={video} />
            ))}
          </div>
          <p className="text-gray-600 text-xs mt-2 flex items-start gap-1">
            <span>ℹ️</span>
            <span>Channel credibility reflects subscriber count and known news outlets only — video content itself is not fact-checked.</span>
          </p>
        </div>
      )}

      {report.sources.length > 0 && (
        <div>
          <h3 className="text-gray-400 text-sm mb-3">Sources reporting on this claim</h3>
          <div className="space-y-2">
            {report.sources.map((source, idx) => (
              <SourceCard key={idx} source={source} />
            ))}
          </div>
        </div>
      )}

      {report.sources.length === 0 && (!report.videos || report.videos.length === 0) && (
        <div className="bg-gray-900 rounded-xl p-6 text-center">
          <p className="text-gray-500 text-sm">
            No recent sources or videos found covering this exact claim. This doesn't necessarily mean it's false — it may just not be widely reported yet.
          </p>
        </div>
      )}
    </div>
  );
}