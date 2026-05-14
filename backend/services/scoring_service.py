"""Scoring service for creator readiness and metrics."""
from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from core.logging import get_logger

logger = get_logger(__name__)


class ScoringService:
    """Service for calculating creator scores and readiness."""

    @staticmethod
    def calculate_upload_consistency(
        upload_history: List[Dict[str, Any]],
    ) -> int:
        """Calculate upload consistency score (0-100).

        Args:
            upload_history: List of upload records

        Returns:
            Consistency score (0-100)
        """
        if not upload_history or len(upload_history) < 2:
            return 50

        # Parse dates and calculate intervals
        intervals = []
        dates = []

        for record in upload_history:
            try:
                if isinstance(record.get("date"), str):
                    date = datetime.fromisoformat(record["date"])
                    dates.append(date)
            except (ValueError, TypeError):
                continue

        if len(dates) < 2:
            return 50

        # Sort by date
        dates.sort()

        # Calculate intervals
        for i in range(1, len(dates)):
            interval = (dates[i] - dates[i - 1]).days
            if interval > 0:
                intervals.append(interval)

        if not intervals:
            return 50

        # Calculate regularity
        avg_interval = sum(intervals) / len(intervals)
        max_interval = max(intervals)
        min_interval = min(intervals)

        # Score based on regularity (penalize large gaps)
        if max_interval == 0:
            return 100

        regularity = max(0, 100 - int((max_interval - avg_interval) / avg_interval * 20))
        return min(100, max(0, regularity))

    @staticmethod
    def calculate_campaign_readiness(
        consistency_score: int,
        engagement_rate: float,
        upload_frequency_days: float = 7.0,
    ) -> str:
        """Calculate campaign readiness status.

        Args:
            consistency_score: Upload consistency score (0-100)
            engagement_rate: Engagement rate as percentage
            upload_frequency_days: Average days between uploads

        Returns:
            Status: "ready", "review", or "pending"
        """
        # Criteria for readiness
        if consistency_score >= 80 and engagement_rate >= 3.5 and upload_frequency_days <= 14:
            return "ready"
        elif consistency_score >= 60 or engagement_rate >= 2.0:
            return "review"
        else:
            return "pending"

    @staticmethod
    def calculate_engagement_trend(
        recent_engagement: float,
        previous_engagement: float,
    ) -> str:
        """Calculate engagement trend.

        Args:
            recent_engagement: Recent engagement rate
            previous_engagement: Previous engagement rate

        Returns:
            Trend: "up" or "down"
        """
        return "up" if recent_engagement >= previous_engagement else "down"

    @staticmethod
    def generate_ai_summary(creator_data: Dict[str, Any]) -> str:
        """Generate AI summary for a creator.

        Args:
            creator_data: Creator data dictionary

        Returns:
            AI-generated summary string
        """
        name = creator_data.get("name", "Creator")
        niche = creator_data.get("niche", "content")
        engagement = creator_data.get("engagement", 0)
        followers = creator_data.get("followers", "Unknown")

        templates = [
            f"High-performing {niche} creator with strong audience connection. Engagement rate of {engagement}% shows dedicated follower base. Ideal for brand partnerships in {niche} space.",
            f"{name} is a trusted {niche} creator with {followers} followers. Consistent content delivery with {engagement}% engagement demonstrates quality audience interaction.",
            f"Premium {niche} content creator attracting {followers} engaged followers. {engagement}% engagement rate indicates influential presence and brand partnership potential.",
            f"Rising star in {niche} category with {followers} subscribers. {engagement}% engagement coupled with regular uploads makes this creator a reliable campaign partner.",
        ]

        return random.choice(templates)

    @staticmethod
    def generate_why_recommended(creator_data: Dict[str, Any], scores: Dict[str, Any]) -> str:
        """Generate recommendation reason.

        Args:
            creator_data: Creator data
            scores: Calculated scores

        Returns:
            Recommendation string
        """
        consistency = scores.get("consistency_score", 50)
        engagement = creator_data.get("engagement", 0)
        followers = creator_data.get("followers_raw", 0)

        reasons = []

        if consistency >= 85:
            reasons.append("Top-tier upload consistency")
        if engagement >= 6.0:
            reasons.append("Exceptional engagement rate")
        if followers >= 1_000_000:
            reasons.append("Large follower base")

        if not reasons:
            reasons = ["Good overall metrics", "Engaged audience"]

        return ". ".join(reasons) + "."
