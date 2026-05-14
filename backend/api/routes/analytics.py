"""Analytics routes."""
from fastapi import APIRouter

from models.schemas import StatsResponse
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """Get analytics statistics.

    Returns:
        Stats response with all metrics
    """
    logger.info("Fetching analytics stats")

    return StatsResponse(
        tracked_creators=12847,
        avg_engagement=5.4,
        active_campaigns=23,
        audits_run=1203,
        weekly_deltas={
            "creators": 324,
            "engagement": 0.8,
            "campaigns": 3,
            "audits": 89,
        },
    )
