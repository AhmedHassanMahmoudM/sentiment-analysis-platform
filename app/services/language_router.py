import re
from langdetect import detect, detect_langs
from app.services.sentiment_service import sentiment_service
from app.services.arabic_sentiment import ArabicSentimentService
from app.services.multilingual_sentiment import multilingual_service

class LanguageRouter:
    def __init__(self):
        self.arabic_service = ArabicSentimentService()
        self.english_service = sentiment_service
        self.multilingual_service = multilingual_service
        
        self.multilingual_langs = {
            "fr", "es", "de", "it", "pt", "nl", "pl", "ru", "tr", "vi", "hi", "zh", "ja", "ko"
        }
    
    def detect_language(self, text: str) -> str:
        """كشف اللغة بالحروف أولاً، وبعدين langdetect"""
        if re.search(r'[\u0600-\u06FF\u0750-\u077F]', text):
            return "ar"
        if re.search(r'[\u0900-\u097F]', text):
            return "hi"
        if re.search(r'[\u0400-\u04FF]', text):
            return "ru"
        if re.search(r'[\u4E00-\u9FFF]', text):
            return "zh"
        if re.search(r'[\u3040-\u309F\u30A0-\u30FF]', text):
            return "ja"
        if re.search(r'[\uAC00-\uD7AF]', text):
            return "ko"
        if re.search(r'[\u0370-\u03FF]', text):
            return "el"
        if re.search(r'[\u0E00-\u0E7F]', text):
            return "th"
        
        try:
            detected = detect_langs(text)
            best = detected[0]
            return best.lang
        except:
            return "en"
    
    def predict_single(self, text: str):
        """تنبؤ لنص واحد مع كشف اللغة"""
        lang = self.detect_language(text)
        
        if lang == "ar":
            result = self.arabic_service.predict(text)
        elif lang == "en":
            result = self.english_service.predict(text)
            result["language"] = "en"
        elif lang in self.multilingual_langs and self.multilingual_service.available:
            result = self.multilingual_service.predict(text, detected_lang=lang)
        else:
            result = self.english_service.predict(text)
            result["language"] = lang
            result["note"] = f"Language '{lang}' not specifically supported. Used English model."
        
        result["detected_language"] = lang
        return result
    
    def predict_batch(self, texts: list[str]):
        """تنبؤ لمجموعة نصوص - كل نص على حسب لغته"""
        results = []
        total_time = 0
        
        for text in texts:
            result = self.predict_single(text)
            total_time += result.get("processing_time_ms", 0)
            results.append({
                "text": text,
                "sentiment": result["sentiment"],
                "confidence": result["confidence"],
                "language": result.get("detected_language", "en"),
                "model_version": result["model_version"]
            })
        
        return results, total_time

router = LanguageRouter()