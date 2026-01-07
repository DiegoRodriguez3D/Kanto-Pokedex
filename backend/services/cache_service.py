"""In-memory cache service with TTL support."""
import time
from typing import Any, Optional


class CacheService:
    """Simple in-memory cache with TTL (Time To Live) support."""
    
    def __init__(self):
        self._cache: dict[str, tuple[Any, float]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from cache if it exists and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None
        
        value, expiry = self._cache[key]
        if time.time() > expiry:
            # Cache expired, remove it
            del self._cache[key]
            return None
        
        return value
    
    def set(self, key: str, value: Any, ttl_seconds: int = 3600) -> None:
        """
        Set a value in cache with TTL.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Time to live in seconds (default: 1 hour)
        """
        expiry = time.time() + ttl_seconds
        self._cache[key] = (value, expiry)
    
    def delete(self, key: str) -> bool:
        """
        Delete a key from cache.
        
        Args:
            key: Cache key
            
        Returns:
            True if key was deleted, False if not found
        """
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
    
    def has(self, key: str) -> bool:
        """
        Check if key exists in cache and hasn't expired.
        
        Args:
            key: Cache key
            
        Returns:
            True if key exists and is valid
        """
        return self.get(key) is not None


# Global cache instance
cache = CacheService()
