from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import time

class ArabicSentimentService:
    def __init__(self):
        # أفضل نموذج عربي - AraBERT v2
        self.model_name = "aubmindlab/bert-base-arabertv2"
        
        print("⏳ جاري تحميل نموذج AraBERT للعربية... (~500MB)")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_name,
            num_labels=3  # Positive, Negative, Neutral
        )
        
        # التصنيفات
        self.labels = ["positive", "negative", "neutral"]
        self.model_version = "arabert-v2"
        
        print("✅ تم تحميل النموذج العربي بنجاح!")
    
    def predict(self, text: str):
        start = time.time()
        
        # Tokenize
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=1)[0]
        
        # Get prediction
        pred_idx = torch.argmax(probabilities).item()
        confidence = float(probabilities[pred_idx])
        
        # Normalize confidence (optional)
        processing_time = (time.time() - start) * 1000
        
        return {
            "sentiment": self.labels[pred_idx],
            "confidence": confidence,
            "processing_time_ms": processing_time,
            "model_version": self.model_version,
            "language": "ar"
        }