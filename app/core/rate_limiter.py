import time
from collections import defaultdict
from fastapi import HTTPException, Request, Depends
from app.core.security import api_key_header, VALID_API_KEYS

class SimpleRateLimiter:
    def __init__(self):
        # requests[api_key] = [timestamp1, timestamp2, ...]
        self.requests = defaultdict(list)
    
    def check(self, api_key: str):
        """نتحقق من الـ Rate Limit"""
        if api_key not in VALID_API_KEYS:
            raise HTTPException(status_code=403, detail="Invalid API Key")
        
        tier_info = VALID_API_KEYS[api_key]
        limit = tier_info["requests_per_minute"]
        
        now = time.time()
        minute_ago = now - 60
        
        # نمسح الطلبات القديمة (أكتر من دقيقة)
        self.requests[api_key] = [
            ts for ts in self.requests[api_key] if ts > minute_ago
        ]
        
        # نتحقق
        if len(self.requests[api_key]) >= limit:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded: {limit} per minute for {tier_info['tier']} tier"
            )
        
        # نسجل الطلب
        self.requests[api_key].append(now)

rate_limiter = SimpleRateLimiter()