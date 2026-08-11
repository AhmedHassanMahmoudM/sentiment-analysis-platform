from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
import secrets

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# في الإنتاج حط الـ Keys في Database أو Env
VALID_API_KEYS = {
    "sk-live-123456789": {"tier": "free", "requests_per_minute": 10},
    "sk-live-premium-abc": {"tier": "premium", "requests_per_minute": 1000},
    "sk-test-demo": {"tier": "demo", "requests_per_minute": 5},
}

def verify_api_key(api_key: str = Security(api_key_header)):
    if not api_key:
        raise HTTPException(status_code=403, detail="API Key required")
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    
    return VALID_API_KEYS[api_key]

def get_rate_limit(api_key: str) -> int:
    return VALID_API_KEYS.get(api_key, {}).get("requests_per_minute", 10)