from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.sentiment import SentimentRequest, BatchSentimentRequest
from app.services.language_router import router as lang_router
from app.services.database_service import db_service
from app.services.cache_service import cache_service
from app.core.database import get_db
from app.core.security import verify_api_key, api_key_header
from app.core.rate_limiter import rate_limiter
from datetime import datetime

router = APIRouter(prefix="/sentiment", tags=["Sentiment Analysis"])


@router.post("/predict")
async def predict_sentiment(
    request: Request,
    body: SentimentRequest, 
    db: Session = Depends(get_db),
    api_key_info: dict = Depends(verify_api_key),
    api_key: str = Depends(api_key_header)
):
    try:
        # ✅ Rate Limit حسب الـ API Key
        rate_limiter.check(api_key)
        
        # Check cache
        cached_result = cache_service.get(body.text)
        if cached_result:
            return {
                "text": body.text,
                "sentiment": cached_result["sentiment"],
                "confidence": cached_result["confidence"],
                "processing_time_ms": 0.5,
                "model_version": cached_result["model_version"],
                "timestamp": datetime.utcnow(),
                "language": cached_result.get("language", "en"),
                "cached": True,
                "tier": api_key_info["tier"]
            }
        
        result = lang_router.predict_single(body.text)
        
        cache_service.set(body.text, {
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "model_version": result["model_version"],
            "language": result.get("detected_language", "en")
        })
        
        db_service.save_prediction(
            db=db,
            text=body.text,
            sentiment=result["sentiment"],
            confidence=result["confidence"],
            language=result.get("detected_language", "en"),
            model_version=result["model_version"],
            processing_time_ms=result["processing_time_ms"]
        )
        
        return {
            "text": body.text,
            "sentiment": result["sentiment"],
            "confidence": result["confidence"],
            "processing_time_ms": result["processing_time_ms"],
            "model_version": result["model_version"],
            "timestamp": datetime.utcnow(),
            "language": result.get("detected_language", "en"),
            "cached": False,
            "tier": api_key_info["tier"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predict/batch")
async def predict_batch(
    request: Request,
    body: BatchSentimentRequest, 
    db: Session = Depends(get_db),
    api_key_info: dict = Depends(verify_api_key),
    api_key: str = Depends(api_key_header)
):
    try:
        # ✅ Rate Limit حسب الـ API Key
        rate_limiter.check(api_key)
        
        results, total_time = lang_router.predict_batch(body.texts)
        
        for item in results:
            db_service.save_prediction(
                db=db,
                text=item["text"],
                sentiment=item["sentiment"],
                confidence=item["confidence"],
                language=item["language"],
                model_version=item["model_version"],
                processing_time_ms=total_time / len(results)
            )
        
        return {
            "results": results,
            "count": len(results),
            "total_processing_time_ms": total_time,
            "timestamp": datetime.utcnow(),
            "tier": api_key_info["tier"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history(request: Request, limit: int = 100, db: Session = Depends(get_db)):
    predictions = db_service.get_recent_predictions(db, limit)
    return {
        "predictions": [
            {
                "id": p.id,
                "text": p.text,
                "sentiment": p.sentiment,
                "confidence": p.confidence,
                "language": p.language,
                "created_at": p.created_at
            }
            for p in predictions
        ],
        "count": len(predictions)
    }


@router.get("/stats")
async def get_stats(request: Request, db: Session = Depends(get_db)):
    return db_service.get_stats(db)