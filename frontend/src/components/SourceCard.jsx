export default function SourceCard({ source }) {
  const title = source.title;
  const sourceName = source.source;
  const date = source.date;
  const snippet = source.snippet;
  const url = source.url;
  const credibility = source.credibility;

  const colorMap = {
    green: 'bg-green-900/30 text-green-400',
    yellow: 'bg-yellow-900/30 text-yellow-400',
    red: 'bg-red-900/30 text-red-400',
  };

  const formattedDate = date
    ? new Date(date).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
    : '';

  const badgeColor = colorMap[credibility.color] || colorMap.yellow;

  return (
    <a href={url} target="_blank" rel="noopener noreferrer" className="block bg-gray-900 rounded-lg p-4 hover:bg-gray-800 transition border border-gray-800">
      <div className="flex justify-between items-start gap-3 mb-2">
        <p className="text-white text-sm font-medium line-clamp-2">{title}</p>
        <span className={`text-xs font-semibold px-2 py-1 rounded whitespace-nowrap ${badgeColor}`}>
          {credibility.label} · {credibility.score}
        </span>
      </div>
      <p className="text-gray-500 text-xs mb-2">{sourceName} · {formattedDate}</p>
      {snippet && <p className="text-gray-400 text-xs line-clamp-2">{snippet}</p>}
    </a>
  );
}