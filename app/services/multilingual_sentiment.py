from transformers import pipeline
import time

class MultilingualSentimentService:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
        self.model_version = "xlm-roberta-multilingual"
        self.available = False
        self.model = None
        
        try:
            print("⏳ جاري تحميل نموذج XLM-RoBERTa متعدد اللغات... (~1.2GB)")
            self.model = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                device=-1
            )
            self.available = True
            print("✅ تم تحميل النموذج متعدد اللغات بنجاح!")
        except Exception as e:
            print(f"⚠️ فشل تحميل النموذج متعدد اللغات: {e}")
            print("   سيتم استخدام النموذج الإنجليزي كـ Fallback")
    
    def predict(self, text: str, detected_lang: str = "unknown"):
        if not self.available:
            # Fallback to English service (will be injected)
            from app.services.sentiment_service import sentiment_service
            result = sentiment_service.predict(text)
            result["note"] = f"Language '{detected_lang}' not supported. Used English model."
            return result
        
        start = time.time()
        result = self.model(text)[0]
        processing_time = (time.time() - start) * 1000
        
        return {
            "sentiment": result["label"].lower(),
            "confidence": result["score"],
            "processing_time_ms": processing_time,
            "model_version": self.model_version,
            "language": detected_lang
        }

multilingual_service = MultilingualSentimentService()