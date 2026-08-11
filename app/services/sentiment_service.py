from transformers import pipeline
from app.core.config import get_settings
import time
import re

class SentimentService:
    def __init__(self):
        settings = get_settings()
        self.model = pipeline(
            "sentiment-analysis",
            model=settings.MODEL_NAME,
            device=-1
        )
        self.model_version = "1.0.0"
    
    def is_arabic(self, text: str) -> bool:
        return bool(re.search(r'[\u0600-\u06FF]', text))
    
    def predict(self, text: str):
        start = time.time()
        
        if self.is_arabic(text):
            return {
                "sentiment": "neutral",
                "confidence": 1.0,
                "processing_time_ms": 0.1,
                "model_version": "arabic-coming-soon",
                "language": "ar",
                "note": "Arabic support will be added in production"
            }
        
        result = self.model(text)[0]
        processing_time = (time.time() - start) * 1000
        
        return {
            "sentiment": result["label"].lower(),
            "confidence": result["score"],
            "processing_time_ms": processing_time,
            "model_version": self.model_version,
            "language": "en"
        }
    
    def predict_batch(self, texts: list[str]):
        start = time.time()
        results = self.model(texts)
        processing_time = (time.time() - start) * 1000
        
        return [
            {
                "text": text,
                "sentiment": r["label"].lower(),
                "confidence": r["score"],
            }
            for text, r in zip(texts, results)
        ], processing_time

sentiment_service = SentimentService()