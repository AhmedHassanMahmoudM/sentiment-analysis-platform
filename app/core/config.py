from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    APP_NAME: str = "Sentiment Analysis API"
    DEBUG: bool = False
    MODEL_NAME: str = "distilbert-base-uncased-finetuned-sst-2-english"
    MAX_LENGTH: int = 512
    
    # Database - يشتغل SQLite للتطوير وPostgreSQL للإنتاج
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sentiment.db")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()