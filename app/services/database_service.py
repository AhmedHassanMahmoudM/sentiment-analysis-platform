from sqlalchemy.orm import Session
from app.models.prediction import Prediction

class DatabaseService:
    def save_prediction(self, db: Session, text: str, sentiment: str, 
                       confidence: float, language: str, 
                       model_version: str, processing_time_ms: float):
        db_prediction = Prediction(
            text=text,
            sentiment=sentiment,
            confidence=confidence,
            language=language,
            model_version=model_version,
            processing_time_ms=processing_time_ms
        )
        db.add(db_prediction)
        db.commit()
        db.refresh(db_prediction)
        return db_prediction
    
    def get_recent_predictions(self, db: Session, limit: int = 100):
        return db.query(Prediction).order_by(Prediction.created_at.desc()).limit(limit).all()
    
    def get_stats(self, db: Session):
        total = db.query(Prediction).count()
        positive = db.query(Prediction).filter(Prediction.sentiment == "positive").count()
        negative = db.query(Prediction).filter(Prediction.sentiment == "negative").count()
        neutral = db.query(Prediction).filter(Prediction.sentiment == "neutral").count()
        
        return {
            "total_predictions": total,
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "positive_percentage": round((positive / total * 100), 2) if total > 0 else 0
        }

db_service = DatabaseService()