from pydantic import BaseModel, Field
from typing import Literal, List
from datetime import datetime


class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class SentimentResponse(BaseModel):
    text: str
    sentiment: Literal["positive", "negative", "neutral"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    processing_time_ms: float
    model_version: str
    timestamp: datetime


class BatchSentimentRequest(BaseModel):
    texts: List[str] = Field(..., min_length=1, max_length=100)


class BatchSentimentResponse(BaseModel):
    results: List[dict]
    count: int
    model_version: str
    timestamp: datetime