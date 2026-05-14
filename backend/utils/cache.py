"""In-memory cache with TTL support."""
import asyncio
import time
from typing import Any, Optional, Dict, Callable

from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)


class CacheEntry:
    """Cache entry with TTL."""

    def __init__(self, value: Any, ttl: int = settings.CACHE_TTL_SECONDS):
        """Initialize cache entry.

        Args:
            value: Cached value
            ttl: Time to live in seconds
        """
        self.value = value
        self.created_at = time.time()
        self.ttl = ttl

    def is_expired(self) -> bool:
        """Check if entry has expired.

        Returns:
            True if expired, False otherwise
        """
        return time.time() - self.created_at > self.ttl


class TTLCache:
    """Simple in-memory TTL cache."""

    def __init__(self):
        """Initialize cache."""
        self._cache: Dict[str, CacheEntry] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found/expired
        """
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if entry.is_expired():
            del self._cache[key]
            return None

        logger.debug(f"Cache hit for key: {key}")
        return entry.value

    def set(self, key: str, value: Any, ttl: int = settings.CACHE_TTL_SECONDS) -> None:
        """Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds
        """
        self._cache[key] = CacheEntry(value, ttl)
        logger.debug(f"Cache set for key: {key}")

    def delete(self, key: str) -> None:
        """Delete value from cache.

        Args:
            key: Cache key
        """
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted for key: {key}")

    def clear(self) -> None:
        """Clear all cache."""
        self._cache.clear()
        logger.debug("Cache cleared")

    def cleanup(self) -> None:
        """Remove expired entries."""
        expired_keys = [
            key for key, entry in self._cache.items() if entry.is_expired()
        ]
        for key in expired_keys:
            del self._cache[key]
        if expired_keys:
            logger.debug(f"Cleaned up {len(expired_keys)} expired cache entries")


# Global cache instance
cache = TTLCache()


def cached(ttl: int = settings.CACHE_TTL_SECONDS):
    """Decorator to cache async function results.

    Args:
        ttl: Time to live in seconds

    Returns:
        Decorator function
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{str(args)}:{str(sorted(kwargs.items()))}"

            # Check cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Call function and cache result
            result = await func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        return wrapper

    return decorator
