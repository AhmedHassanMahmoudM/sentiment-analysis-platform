from fastapi import FastAPI
from app.api.v1.endpoints import sentiment
from app.core.config import get_settings
from app.core.database import init_db

settings = get_settings()
init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    docs_url="/docs"
)

app.include_router(sentiment.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {"message": "Sentiment Analysis API", "docs": "/docs"}