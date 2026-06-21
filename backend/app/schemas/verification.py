# backend/app/schemas/verification.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class SourceCredibility(BaseModel):
    score: int
    label: str
    color: str


class NewsSource(BaseModel):
    title: str
    url: str
    domain: str
    source: str
    date: str
    snippet: str
    credibility: SourceCredibility


class VerificationRequest(BaseModel):
    news_text: str


class VerificationResponse(BaseModel):
    claim: str
    ml_prediction: str
    ml_confidence: float
    credibility_score: int
    verdict: str
    explanation: str
    sources_found: int
    sources: List[NewsSource]
    verified_at: str

class YouTubeVideo(BaseModel):
    title: str
    channel: str
    video_id: str
    url: str
    thumbnail: str
    published_at: str
    subscriber_count: int
    credibility_tier: str
    credibility_color: str
    is_trusted_channel: bool


class VerificationResponse(BaseModel):
    claim: str
    ml_prediction: str
    ml_confidence: float
    credibility_score: int
    verdict: str
    explanation: str
    sources_found: int
    sources: List[NewsSource]
    videos_found: int
    videos: List[YouTubeVideo]
    verified_at: str