"""Health check routes."""
from fastapi import APIRouter, Depends

from core.config import settings
from models.schemas import HealthResponse
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Health status
    """
    ytdlp_available = settings.YTDLP_ENABLED

    return HealthResponse(
        status="ok",
        version=settings.APP_VERSION,
        youtube_api_ok=bool(settings.YOUTUBE_API_KEY),
        ytdlp_available=ytdlp_available,
        database_ok=True,
    )
