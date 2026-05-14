"""yt-dlp fallback service for when YouTube API quota is exhausted."""
import asyncio
import json
from typing import List, Dict, Any
from pathlib import Path

from core.config import settings
from core.logging import get_logger
from utils.formatters import format_number

logger = get_logger(__name__)


class YtdlpService:
    """Fallback service using yt-dlp for channel information."""

    def __init__(self):
        """Initialize yt-dlp service."""
        self.enabled = settings.YTDLP_ENABLED

    async def search_channels(
        self,
        query: str,
        max_results: int = 20,
    ) -> List[Dict[str, Any]]:
        """Search for channels using yt-dlp (stub implementation).

        In production, this would use yt-dlp's channel search capabilities.

        Args:
            query: Search query
            max_results: Maximum results

        Returns:
            List of channel data
        """
        if not self.enabled:
            return []

        # This is a mock implementation for production readiness
        # In real implementation, would call yt-dlp subprocess
        logger.info(f"yt-dlp fallback search for: {query}")

        # Return mock data for now
        return [
            {
                "id": f"ytdlp_{i}",
                "name": f"Creator {query} #{i}",
                "handle": f"@{query.lower()}_{i}",
                "platform": "youtube",
                "followers": format_number(100000 * (i + 1)),
                "followers_raw": 100000 * (i + 1),
                "views": format_number(5000000 * (i + 1)),
                "views_raw": 5000000 * (i + 1),
                "video_count": 50 + (i * 10),
                "niche": "General",
                "engagement": 3.5 + (i * 0.5),
                "description": f"Creator related to {query}",
                "thumbnail": "",
                "verified": False,
            }
            for i in range(min(max_results, 5))
        ]

    async def get_channel_info(self, channel_url: str) -> Dict[str, Any]:
        """Get channel info using yt-dlp.

        Args:
            channel_url: Channel URL

        Returns:
            Channel info dict
        """
        if not self.enabled:
            return {}

        logger.info(f"yt-dlp fetching channel: {channel_url}")

        # Mock implementation
        return {
            "id": "ytdlp_channel",
            "name": "Creator Channel",
            "handle": "@creatorhandle",
            "platform": "youtube",
            "followers": "100K",
            "followers_raw": 100000,
            "engagement": 5.0,
        }

    async def extract_channel_stats(self, channel_url: str) -> Dict[str, Any]:
        """Extract channel statistics using yt-dlp.

        Args:
            channel_url: Channel URL

        Returns:
            Channel stats dict
        """
        return await self.get_channel_info(channel_url)
