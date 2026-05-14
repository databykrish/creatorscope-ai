"""Pydantic models for Creator data."""
from pydantic import BaseModel, Field
from typing import Optional, List


class Creator(BaseModel):
    """Creator profile model - matches frontend interface exactly."""

    id: str = Field(..., description="Unique creator ID")
    name: str = Field(..., description="Creator's real name")
    handle: str = Field(..., description="Creator's handle (e.g., @kaitech)")
    avatar: str = Field(default="", description="Avatar URL")
    platform: str = Field(..., description="Platform: instagram|youtube|tiktok")
    followers: str = Field(..., description="Formatted follower count (e.g., '1.1M')")
    engagement: float = Field(..., description="Engagement rate percentage")
    engagementTrend: str = Field(default="up", description="Trend: up|down")
    uploadConsistency: int = Field(default=50, ge=0, le=100, description="Consistency score 0-100")
    campaignReady: str = Field(default="pending", description="Status: ready|review|pending")
    niche: str = Field(..., description="Creator's primary niche")
    aiSummary: str = Field(default="", description="AI-generated summary paragraph")
    whyRecommended: str = Field(default="", description="Why this creator is recommended")
    recentPosts: int = Field(default=0, description="Number of recent posts")
    avgViews: str = Field(default="0", description="Formatted average views (e.g., '420K')")

    class Config:
        """Pydantic config."""
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "Kai Nakamura",
                "handle": "@kaitech",
                "avatar": "",
                "platform": "youtube",
                "followers": "1.1M",
                "engagement": 6.2,
                "engagementTrend": "up",
                "uploadConsistency": 88,
                "campaignReady": "ready",
                "niche": "Tech",
                "aiSummary": "Trusted tech reviewer with deep audience trust signals.",
                "whyRecommended": "Audience overlap with target demo is 78%.",
                "recentPosts": 12,
                "avgViews": "420K",
            }
        }


class CreatorSearchResponse(BaseModel):
    """Creator search response."""

    creators: List[Creator] = Field(..., description="List of creators")
    total: int = Field(..., description="Total results")
    source: str = Field(default="youtube_api", description="Data source: youtube_api|ytdlp|cached")
    fallback_used: bool = Field(default=False, description="Whether fallback was used")


class AuditResult(BaseModel):
    """Creator audit result."""

    creator_id: str = Field(..., description="Creator ID")
    upload_history: list[dict] = Field(default_factory=list, description="Upload history")
    consistency_trend: str = Field(default="stable", description="Consistency trend")
    engagement_trend: list[float] = Field(default_factory=list, description="Engagement trend")
    risk_flags: list[str] = Field(default_factory=list, description="Risk flags")
    last_audit_date: str = Field(..., description="ISO format date")


class StatsResponse(BaseModel):
    """Analytics stats response."""

    tracked_creators: int = Field(..., description="Total tracked creators")
    avg_engagement: float = Field(..., description="Average engagement rate")
    active_campaigns: int = Field(..., description="Active campaigns count")
    audits_run: int = Field(..., description="Total audits run")
    weekly_deltas: dict = Field(
        default_factory=dict,
        description="Weekly changes"
    )


class ExportRequest(BaseModel):
    """Export request model."""

    creator_ids: List[str] = Field(..., description="List of creator IDs to export")
    format: str = Field(default="csv", description="Format: csv|json|pdf")


class ExportResponse(BaseModel):
    """Export response model."""

    export_id: str = Field(..., description="Export ID")
    download_url: str = Field(..., description="Download URL")
    expires_at: str = Field(..., description="ISO format expiration date")
    status: str = Field(default="pending", description="Status: pending|ready|expired")


class LogEntry(BaseModel):
    """Console log entry."""

    timestamp: str = Field(..., description="ISO format timestamp")
    type: str = Field(..., description="Log type: info|success|warning|process")
    message: str = Field(..., description="Log message")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(default="ok")
    version: str = Field(...)
    youtube_api_ok: bool = Field(default=False)
    ytdlp_available: bool = Field(default=False)
    database_ok: bool = Field(default=False)


class ErrorResponse(BaseModel):
    """Standard error response."""

    error: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: dict = Field(default_factory=dict, description="Additional details")
    fallback_used: bool = Field(default=False, description="Whether fallback was used")
