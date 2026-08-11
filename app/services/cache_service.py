import redis
import json
import hashlib
import os

class CacheService:
    def __init__(self):
        try:
            self.client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                db=0,
                decode_responses=True
            )
            self.client.ping()
            self.available = True
            print("✅ Redis connected")
        except Exception as e:
            print(f"⚠️ Redis not available: {e}")
            self.available = False
    
    def _generate_key(self, text: str) -> str:
        hash_object = hashlib.md5(text.encode())
        return f"sentiment:{hash_object.hexdigest()}"
    
    def get(self, text: str):
        if not self.available:
            return None
        key = self._generate_key(text)
        cached = self.client.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def set(self, text: str, result: dict, expire: int = 3600):
        if not self.available:
            return
        key = self._generate_key(text)
        self.client.setex(key, expire, json.dumps(result))
    
    def clear(self):
        if self.available:
            self.client.flushdb()

cache_service = CacheService()