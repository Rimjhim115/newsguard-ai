# backend/app/schemas/prediction.py
# PURPOSE: Pydantic schemas for Prediction data.
#
# PredictionRequest → client sends news text to analyze
# PredictionResponse → we send back the result

from pydantic import BaseModel
from datetime import datetime


class PredictionRequest(BaseModel):
    """
    What the client sends for news verification.
    Just the raw news text — nothing else needed.
    """
    news_text: str


class PredictionResponse(BaseModel):
    """
    What we send back after analyzing the news.
    Includes the prediction result and confidence score.
    """
    id: int
    news_text: str
    prediction: str       # "REAL" or "FAKE"
    confidence: float     # 0.0 to 1.0
    created_at: datetime

    class Config:
        from_attributes = True