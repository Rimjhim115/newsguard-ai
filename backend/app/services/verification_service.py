# backend/app/services/verification_service.py
# PURPOSE: Real-time news verification using DuckDuckGo search.
# Searches for the claim, analyzes sources, returns credibility report.

from ddgs import DDGS
from datetime import datetime
from typing import List, Dict
from googleapiclient.discovery import build
from app.config import settings

# Source credibility database
# Score 0-100: higher = more credible
TRUSTED_SOURCES = {
    # International
    "reuters.com": 95,
    "apnews.com": 94,
    "bbc.com": 92,
    "bbc.co.uk": 92,
    "theguardian.com": 88,
    "nytimes.com": 87,
    "washingtonpost.com": 86,
    "bloomberg.com": 88,
    "economist.com": 90,

    "msn.com": 72,
    "moneycontrol.com": 75,
    "theweek.in": 74,
    "mathrubhumi.com": 72,
    "deccanherald.com": 78,
    "tribuneindia.com": 76,
    "freepressjournal.in": 68,
    "outlookindia.com": 76,
    "thequint.com": 74,
    "wionews.com": 72,
    "republicworld.com": 65,
    "opindia.com": 40,
    "swarajyamag.com": 55,
    

    "economictimes.indiatimes.com": 80,
    "indiatimes.com": 75,
    # Northeast specific
    "pratidintime.com": 68,
    "nagalandpost.com": 68,
    "morungexpress.com": 68,
    "ifp.co.in": 65,
    "uniindia.com": 72,
    "aninews.in": 75,
    "pti.in": 85,
    
    # Indian national
    "ndtv.com": 82,
    "thehindu.com": 85,
    "hindustantimes.com": 80,
    "indianexpress.com": 83,
    "timesofindia.com": 78,
    "livemint.com": 80,
    "businessstandard.com": 82,
    "scroll.in": 78,
    "thewire.in": 75,
    "firstpost.com": 74,
    "indiatodayne.in": 76,
    
    # Northeast India
    "sentinelassam.com": 72,
    "telegraphindia.com": 78,
    "assamtribune.com": 70,
    "nenow.in": 68,
    "eastmojo.com": 70,
    
    # Government/Official
    "pib.gov.in": 99,
    "mha.gov.in": 99,
    "nasa.gov": 99,
    "who.int": 97,
    "un.org": 96,
    
    # TV News
    "abplive.com": 75,
    "zeenews.india.com": 72,
    "indiatoday.in": 78,
    "aajtak.in": 72,
    "news18.com": 74,
}

TRUSTED_YOUTUBE_CHANNELS = [
    "ndtv", "abp news", "aaj tak", "india today", "republic",
    "bbc news", "reuters", "cnn", "al jazeera english",
    "zee news", "news18", "times now", "the hindu",
    "wion", "dd news", "doordarshan", "pratidin time",
    "news live assam", "prag news",
]

# Known fake/unreliable sources
UNRELIABLE_SOURCES = [
    "worldnewsdailyreport.com",
    "empirenews.net",
    "nationalreport.net",
    "huzlers.com",
    "theonion.com",
]


def get_domain(url: str) -> str:
    """Extract domain from URL."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
        # Remove www.
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except:
        return ""


def get_source_credibility(url: str) -> Dict:
    """
    Score a source's credibility based on domain.
    Returns score and label.
    """
    domain = get_domain(url)

    # Check if unreliable
    for unreliable in UNRELIABLE_SOURCES:
        if unreliable in domain:
            return {
                "score": 5,
                "label": "Unreliable",
                "color": "red"
            }

    # Check trusted sources — improved matching
    # Sort by length descending so more specific matches win first
    for source, score in sorted(TRUSTED_SOURCES.items(), key=lambda x: -len(x[0])):
        if source in domain or domain in source:
            if score >= 90:
                label = "Highly Credible"
                color = "green"
            elif score >= 75:
                label = "Credible"
                color = "green"
            elif score >= 60:
                label = "Moderate"
                color = "yellow"
            else:
                label = "Low Credibility"
                color = "red"
            return {
                "score": score,
                "label": label,
                "color": color
            }

    return {
        "score": 50,
        "label": "Unknown",
        "color": "yellow"
    }


def search_news(claim: str, max_results: int = 8) -> List[Dict]:
    """Search DuckDuckGo for RECENT news only — never return old articles."""
    import time

    stopwords = {"the", "a", "an", "is", "are", "was", "were", "today", 
                 "in", "on", "at", "to", "of", "and", "for", "this", "that",
                 "hits", "news", "latest"}
    claim_words = [w.lower().strip(".,!?") for w in claim.split() 
                   if w.lower() not in stopwords and len(w) > 2]

    def is_topic_page(url: str) -> bool:
        markers = ["/topic/", "/tag/", "/tags/", "/topics/"]
        return any(m in url.lower() for m in markers)

    def is_relevant(item):
        url = item.get("url") or item.get("href", "")
        if is_topic_page(url):
            return False
        title = item.get("title", "").lower()
        matches = sum(1 for w in claim_words if w in title)
        return matches == len(claim_words)

    # Try news search first — strictly limited to last week
    raw_results = []
    for attempt in range(3):
        try:
            with DDGS() as ddgs:
                raw_results = list(ddgs.news(
                    query=claim,
                    max_results=max_results * 3,
                    timelimit="w"   # last week ONLY
                ))
                if raw_results:
                    break
                time.sleep(2)
        except Exception as e:
            print(f"DuckDuckGo news attempt {attempt + 1} failed: {e}")
            time.sleep(3)

    filtered = [r for r in raw_results if is_relevant(r)] if claim_words else raw_results
    if filtered:
        return filtered[:max_results]

    # Fallback: text search, but STILL restricted to last week
    try:
        with DDGS() as ddgs:
            text_results = list(ddgs.text(
                query=f"{claim} news",
                max_results=max_results * 3,
                timelimit="w"   # last week ONLY — same restriction
            ))
            filtered_text = [r for r in text_results if is_relevant(r)] if claim_words else text_results
            return filtered_text[:max_results]
    except Exception as e:
        print(f"DuckDuckGo text search failed: {e}")
        return []

def search_youtube(claim: str, max_results: int = 5) -> List[Dict]:
    """Search YouTube for news videos covering this claim."""
    if not settings.YOUTUBE_API_KEY:
        return []

    try:
        youtube = build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)

        from datetime import datetime, timedelta
        published_after = (datetime.utcnow() - timedelta(days=14)).isoformat("T") + "Z"

        search_request = youtube.search().list(
            q=claim,
            part="snippet",
            type="video",
            order="date",
            maxResults=max_results,
            relevanceLanguage="en",
            publishedAfter=published_after
        )
        search_response = search_request.execute()

        if not search_response.get("items"):
            return []

        channel_ids = list(set(
            item["snippet"]["channelId"] for item in search_response["items"]
        ))

        channels_request = youtube.channels().list(
            part="statistics",
            id=",".join(channel_ids)
        )
        channels_response = channels_request.execute()

        channel_info = {}
        for ch in channels_response.get("items", []):
            sub_count = int(ch["statistics"].get("subscriberCount", 0))
            channel_info[ch["id"]] = {"subscriber_count": sub_count}

        videos = []
        for item in search_response["items"]:
            channel_id = item["snippet"]["channelId"]
            channel_title = item["snippet"]["channelTitle"]
            info = channel_info.get(channel_id, {"subscriber_count": 0})

            is_known_trusted = any(
                trusted in channel_title.lower()
                for trusted in TRUSTED_YOUTUBE_CHANNELS
            )

            sub_count = info["subscriber_count"]
            if is_known_trusted and sub_count >= 1_000_000:
                tier = "Verified News Outlet"
                color = "green"
            elif sub_count >= 500_000:
                tier = "Established Channel"
                color = "green"
            elif sub_count >= 50_000:
                tier = "Moderate Reach"
                color = "yellow"
            else:
                tier = "Small/Unknown Channel"
                color = "red"

            videos.append({
                "title": item["snippet"]["title"],
                "channel": channel_title,
                "video_id": item["id"]["videoId"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"],
                "published_at": item["snippet"]["publishedAt"],
                "subscriber_count": sub_count,
                "credibility_tier": tier,
                "credibility_color": color,
                "is_trusted_channel": is_known_trusted
            })

        videos.sort(key=lambda v: (v["is_trusted_channel"], v["subscriber_count"]), reverse=True)
        return videos

    except Exception as e:
        print(f"YouTube search error: {e}")
        return []

def calculate_credibility_score(
    sources: List[Dict],
    ml_prediction: str,
    ml_confidence: float
) -> Dict:
    """
    Calculate overall credibility score.
    
    Source evidence is weighted far more heavily than the ML model,
    since the ML model was trained on a narrow domain (2016-2018 
    US political news) and is unreliable outside that scope.
    ML acts as a tie-breaker/secondary signal, not a primary one.
    """
    if not sources:
        # No sources found — ML is all we have, but flag it clearly
        ml_score = ml_confidence * 100 if ml_prediction == "REAL" else (1 - ml_confidence) * 100
        return {
            "score": int(ml_score * 0.3),
            "verdict": "UNVERIFIED",
            "explanation": "No recent news sources found covering this claim. ML model alone is unreliable — treat with caution."
        }

    source_scores = [s["credibility"]["score"] for s in sources]
    avg_source_score = sum(source_scores) / len(source_scores)

    highly_credible = len([s for s in sources if s["credibility"]["score"] >= 80])
    credible_count_score = min(highly_credible * 25, 100)

    unique_domains = len(set([s["domain"] for s in sources]))
    diversity_score = min(unique_domains * 15, 100)

    if ml_prediction == "REAL":
        ml_score = ml_confidence * 100
    else:
        ml_score = (1 - ml_confidence) * 100

    # NEW WEIGHTING: source evidence dominates, ML is a minor signal
    final_score = int(
        ml_score * 0.10 +              # ML: 30% → 10%
        avg_source_score * 0.50 +      # sources: 40% → 50%
        credible_count_score * 0.25 +  # credible count: 20% → 25%
        diversity_score * 0.15         # diversity: 10% → 15%
    )

    if final_score >= 75:
        verdict = "CREDIBLE"
    elif final_score >= 50:
        verdict = "POSSIBLY CREDIBLE"
    elif final_score >= 30:
        verdict = "QUESTIONABLE"
    else:
        verdict = "NOT CREDIBLE"

    if highly_credible >= 3:
        explanation = f"Multiple credible sources ({highly_credible}) including major outlets have reported on this claim."
    elif highly_credible >= 1:
        explanation = f"Some credible sources found ({highly_credible}). Verify with additional sources."
    elif len(sources) > 0:
        explanation = "Found in low-credibility sources only. Treat with caution."
    else:
        explanation = "No credible sources found covering this claim."

    # Note: ML prediction shown separately in UI, not hidden,
    # but doesn't dominate the score when real evidence exists
    if ml_prediction == "FAKE" and final_score >= 60:
        explanation += " Note: our ML model flagged this as FAKE based on writing style, but real-time sources strongly support its credibility — the ML model's training data does not cover this topic well."

    return {
        "score": final_score,
        "verdict": verdict,
        "explanation": explanation
    }


def verify_news(
    claim: str,
    ml_prediction: str,
    ml_confidence: float
) -> Dict:
    """Main verification function. Combines DuckDuckGo + YouTube + ML."""
    raw_results = search_news(claim)
    youtube_videos = search_youtube(claim)

    processed_sources = []
    for result in raw_results:
        # ddgs.news() uses 'url' and 'source'
        # ddgs.text() uses 'href' instead of 'url', no 'source' field
        url = result.get("url") or result.get("href", "")
        domain = get_domain(url)
        credibility = get_source_credibility(url)
        source_name = result.get("source") or domain or "Unknown"

        processed_sources.append({
            "title": result.get("title", ""),
            "url": url,
            "domain": domain,
            "source": source_name,
            "date": result.get("date", ""),
            "snippet": result.get("body", "")[:200],
            "credibility": credibility
        })

    processed_sources.sort(key=lambda x: x["credibility"]["score"], reverse=True)

    credibility_report = calculate_credibility_score(
        processed_sources,
        ml_prediction,
        ml_confidence
    )

    trusted_video_count = len([v for v in youtube_videos if v["is_trusted_channel"]])
    if trusted_video_count > 0:
        credibility_report["score"] = min(100, credibility_report["score"] + (trusted_video_count * 5))
        credibility_report["explanation"] += f" Also covered by {trusted_video_count} trusted news channel(s) on YouTube."

    return {
        "claim": claim,
        "ml_prediction": ml_prediction,
        "ml_confidence": round(ml_confidence * 100, 1),
        "credibility_score": credibility_report["score"],
        "verdict": credibility_report["verdict"],
        "explanation": credibility_report["explanation"],
        "sources_found": len(processed_sources),
        "sources": processed_sources[:6],
        "videos_found": len(youtube_videos),
        "videos": youtube_videos[:4],
        "verified_at": datetime.utcnow().isoformat()
    }