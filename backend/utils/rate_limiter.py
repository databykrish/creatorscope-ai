"""Rate limiting for API calls."""
import asyncio
import time
from typing import Callable, Any

from core.config import settings
from core.logging import get_logger

logger = get_logger(__name__)


class YouTubeRateLimiter:
    """Rate limiter for YouTube API calls.

    Enforces a mandatory delay between API calls to respect rate limits
    and avoid triggering YouTube's anti-scraping detection.
    """

    _last_call: float = 0.0
    _delay: float = settings.RATE_LIMIT_DELAY_SECONDS

    @classmethod
    async def wait(cls) -> None:
        """Wait the required time before the next API call."""
        now = time.monotonic()
        elapsed = now - cls._last_call

        if elapsed < cls._delay:
            sleep_time = cls._delay - elapsed
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)

        cls._last_call = time.monotonic()


async def rate_limited(func: Callable[..., Any]) -> Any:
    """Decorator to rate-limit a coroutine function.

    Args:
        func: Async function to wrap

    Returns:
        Wrapped function that enforces rate limiting
    """

    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        await YouTubeRateLimiter.wait()
        return await func(*args, **kwargs)

    return wrapper
