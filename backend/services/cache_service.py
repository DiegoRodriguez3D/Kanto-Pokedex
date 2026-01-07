"""In-memory cache service with TTL support."""
import time
from typing import Any, Optional


class CacheService:
    """Simple in-memory cache with TTL (Time To Live) support."""
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value or None if not found/expired."""
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        if time.time() > expiry:
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """Store value with TTL (default: 1 hour)."""
        expiry = time.time() + ttl_seconds
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> bool:
        """Remove key from cache. Returns True if deleted."""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """Check if key exists and hasn't expired."""
        return self.get(key) is not None


cache = CacheService()
