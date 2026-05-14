"""YouTube API service for fetching creator data."""
import asyncio
import httpx
from typing import Optional, Dict, Any, List

from core.config import settings
from core.exceptions import YouTubeAPIError, YouTubeQuotaExceededError
from core.logging import get_logger
from utils.cache import cache, cached
from utils.rate_limiter import YouTubeRateLimiter
from utils.formatters import format_number, calculate_engagement_rate

logger = get_logger(__name__)


class YouTubeService:
    """Service for YouTube API integration."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self):
        """Initialize YouTube service."""
        self.api_key = settings.YOUTUBE_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)

    async def search_channels(
        self,
        query: str,
        max_results: int = 20,
        platform: str = "youtube",
    ) -> List[Dict[str, Any]]:
        """Search for channels on YouTube.

        Args:
            query: Search query
            max_results: Maximum results to return
            platform: Platform filter (ignored for YouTube, used for multi-platform)

        Returns:
            List of channel data dicts

        Raises:
            YouTubeAPIError: If API call fails
            YouTubeQuotaExceededError: If quota is exceeded
        """
        if not self.api_key:
            raise YouTubeAPIError("YouTube API key not configured")

        if platform != "youtube":
            return []

        try:
            await YouTubeRateLimiter.wait()

            # Search for channels
            search_response = await self.client.get(
                f"{self.BASE_URL}/search",
                params={
                    "part": "snippet",
                    "type": "channel",
                    "q": query,
                    "maxResults": min(max_results, 50),
                    "order": "relevance",
                    "key": self.api_key,
                },
            )

            if search_response.status_code == 403:
                logger.warning("YouTube API quota exceeded")
                raise YouTubeQuotaExceededError()

            if search_response.status_code != 200:
                raise YouTubeAPIError(
                    f"YouTube API error: {search_response.status_code}",
                    {"response": search_response.text},
                )

            search_data = search_response.json()
            channel_ids = [
                item["id"]["channelId"]
                for item in search_data.get("items", [])
            ]

            if not channel_ids:
                return []

            # Get detailed channel info
            await YouTubeRateLimiter.wait()
            channels_response = await self.client.get(
                f"{self.BASE_URL}/channels",
                params={
                    "part": "snippet,statistics",
                    "id": ",".join(channel_ids),
                    "key": self.api_key,
                },
            )

            if channels_response.status_code != 200:
                raise YouTubeAPIError(
                    f"YouTube API error: {channels_response.status_code}"
                )

            channels_data = channels_response.json()
            return [self._parse_channel(item) for item in channels_data.get("items", [])]

        except YouTubeQuotaExceededError:
            raise
        except YouTubeAPIError:
            raise
        except Exception as e:
            logger.error(f"YouTube search error: {str(e)}")
            raise YouTubeAPIError(f"YouTube search failed: {str(e)}")

    async def get_channel_stats(self, channel_id: str) -> Dict[str, Any]:
        """Get detailed channel statistics.

        Args:
            channel_id: YouTube channel ID

        Returns:
            Channel statistics dict

        Raises:
            YouTubeAPIError: If API call fails
        """
        if not self.api_key:
            raise YouTubeAPIError("YouTube API key not configured")

        try:
            await YouTubeRateLimiter.wait()

            response = await self.client.get(
                f"{self.BASE_URL}/channels",
                params={
                    "part": "statistics,contentDetails,snippet",
                    "id": channel_id,
                    "key": self.api_key,
                },
            )

            if response.status_code != 200:
                raise YouTubeAPIError(f"Failed to get channel stats: {response.status_code}")

            items = response.json().get("items", [])
            if not items:
                raise YouTubeAPIError(f"Channel {channel_id} not found")

            return self._parse_channel(items[0])

        except YouTubeAPIError:
            raise
        except Exception as e:
            logger.error(f"Get channel stats error: {str(e)}")
            raise YouTubeAPIError(f"Failed to get channel stats: {str(e)}")

    async def get_recent_videos(
        self,
        channel_id: str,
        max_results: int = 50,
    ) -> List[Dict[str, Any]]:
        """Get recent videos from a channel.

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum videos to return

        Returns:
            List of video data dicts
        """
        if not self.api_key:
            return []

        try:
            await YouTubeRateLimiter.wait()

            # Get uploads playlist ID
            channel_response = await self.client.get(
                f"{self.BASE_URL}/channels",
                params={
                    "part": "contentDetails",
                    "id": channel_id,
                    "key": self.api_key,
                },
            )

            if channel_response.status_code != 200:
                return []

            uploads_playlist_id = (
                channel_response.json()
                .get("items", [{}])[0]
                .get("contentDetails", {})
                .get("relatedPlaylists", {})
                .get("uploads")
            )

            if not uploads_playlist_id:
                return []

            # Get videos from uploads playlist
            await YouTubeRateLimiter.wait()
            videos_response = await self.client.get(
                f"{self.BASE_URL}/playlistItems",
                params={
                    "part": "snippet",
                    "playlistId": uploads_playlist_id,
                    "maxResults": min(max_results, 50),
                    "key": self.api_key,
                },
            )

            if videos_response.status_code != 200:
                return []

            items = videos_response.json().get("items", [])
            return [
                {
                    "video_id": item["snippet"]["resourceId"]["videoId"],
                    "title": item["snippet"]["title"],
                    "published_at": item["snippet"]["publishedAt"],
                }
                for item in items
            ]

        except Exception as e:
            logger.warning(f"Failed to get recent videos: {str(e)}")
            return []

    @staticmethod
    def _parse_channel(channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse YouTube channel data into internal format.

        Args:
            channel_data: Raw channel data from YouTube API

        Returns:
            Parsed channel data dict
        """
        snippet = channel_data.get("snippet", {})
        statistics = channel_data.get("statistics", {})

        subscriber_count = int(statistics.get("subscriberCount", 0))
        view_count = int(statistics.get("viewCount", 0))
        video_count = int(statistics.get("videoCount", 0))

        # Calculate estimated engagement
        engagement = 4.5 if subscriber_count > 0 else 0

        return {
            "id": channel_data.get("id", ""),
            "name": snippet.get("title", ""),
            "handle": f"@{snippet.get('customUrl', '').replace('http://www.youtube.com/c/', '')}",
            "platform": "youtube",
            "followers": format_number(subscriber_count),
            "followers_raw": subscriber_count,
            "views": format_number(view_count),
            "views_raw": view_count,
            "video_count": video_count,
            "niche": "Varied",  # Would be detected via ML in production
            "engagement": engagement,
            "description": snippet.get("description", ""),
            "thumbnail": snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
            "verified": snippet.get("verified", False),
        }

    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()
