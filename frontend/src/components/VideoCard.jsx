export default function VideoCard({ video }) {
  const colorMap = {
    green: 'bg-green-900/30 text-green-400',
    yellow: 'bg-yellow-900/30 text-yellow-400',
    red: 'bg-red-900/30 text-red-400',
  };

  const formattedDate = video.published_at ? new Date(video.published_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : '';

  let subDisplay = video.subscriber_count + ' subs';
  if (video.subscriber_count >= 1000000) {
    subDisplay = (video.subscriber_count / 1000000).toFixed(1) + 'M subs';
  } else if (video.subscriber_count >= 1000) {
    subDisplay = Math.round(video.subscriber_count / 1000) + 'K subs';
  }

  const badgeColor = colorMap[video.credibility_color] || colorMap.yellow;

  return (
    <a href={video.url} target="_blank" rel="noopener noreferrer" className="block bg-gray-900 rounded-lg overflow-hidden border border-gray-800 hover:border-gray-600 transition">
      <div className="relative">
        <img src={video.thumbnail} alt={video.title} className="w-full aspect-video object-cover" />
        <span className="absolute bottom-2 right-2 bg-black/75 text-white text-[10px] px-2 py-0.5 rounded">YouTube</span>
      </div>
      <div className="p-3">
        <p className="text-white text-sm font-medium line-clamp-2 mb-2">{video.title}</p>
        <div className="flex justify-between items-center">
          <span className="text-gray-500 text-xs">{video.channel} · {subDisplay}</span>
          <span className={`text-[10px] px-2 py-0.5 rounded whitespace-nowrap ${badgeColor}`}>{video.credibility_tier}</span>
        </div>
        {formattedDate && <p className="text-gray-600 text-[11px] mt-1">{formattedDate}</p>}
      </div>
    </a>
  );
}