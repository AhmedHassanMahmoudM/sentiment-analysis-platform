import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.rate_limiter import rate_limiter

@pytest.fixture
def client():
    # نمسح الـ Rate Limit قبل كل Test
    rate_limiter.requests.clear()
    return TestClient(app)

@pytest.fixture
def demo_key():
    return {"X-API-Key": "sk-test-demo"}

@pytest.fixture
def premium_key():
    return {"X-API-Key": "sk-live-premium-abc"}