"""Creator search and management routes."""
from fastapi import APIRouter, Query
from typing import List, Optional

from models.schemas import Creator, CreatorSearchResponse, AuditResult
from services.youtube_service import YouTubeService
from services.ytdlp_service import YtdlpService
from services.scoring_service import ScoringService
from utils.formatters import format_number
from utils.cache import cache
from core.logging import get_logger
from core.exceptions import InvalidSearchQueryError, CreatorNotFoundError

logger = get_logger(__name__)
router = APIRouter(prefix="/api/creators", tags=["creators"])

# Service instances
youtube_service = YouTubeService()
ytdlp_service = YtdlpService()
scoring_service = ScoringService()


@router.get("/search", response_model=CreatorSearchResponse)
async def search_creators(
    q: str = Query(default="", min_length=0, max_length=100),
    platform: str = Query(default="youtube", regex="^(youtube|instagram|tiktok|all)$"),
    niche: Optional[str] = Query(default=None),
    sort: str = Query(default="relevance", regex="^(relevance|engagement|followers)$"),
    limit: int = Query(default=20, ge=1, le=50),
) -> CreatorSearchResponse:
    """Search for creators.

    Args:
        q: Search query (optional, empty returns mock data for tracked creators)
        platform: Platform filter
        niche: Niche filter (optional)
        sort: Sort order
        limit: Results limit

    Returns:
        Search results with creators

    Raises:
        InvalidSearchQueryError: If query is invalid
    """
    try:
        # If empty query, return tracked creators (mock data for now)
        if not q or q.strip() == "":
            # Return tracked creators list (mock data)
            return CreatorSearchResponse(
                creators=[],
                total=0,
                source="tracked",
                fallback_used=False,
            )

        # Check cache first
        cache_key = f"search:{q}:{platform}:{limit}"
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        # Search for creators
        creators_data = []
        fallback_used = False
        source = "youtube_api"

        try:
            if platform in ["youtube", "all"]:
                youtube_results = await youtube_service.search_channels(
                    q, max_results=limit, platform="youtube"
                )
                creators_data.extend(youtube_results)
                source = "youtube_api"

        except Exception as e:
            logger.info(f"YouTube API unavailable (API key may not be configured), using yt-dlp scraper: {str(e)}")
            fallback_used = True
            source = "ytdlp"

            # Try yt-dlp fallback
            try:
                ytdlp_results = await ytdlp_service.search_channels(q, max_results=limit)
                creators_data.extend(ytdlp_results)
            except Exception as e2:
                logger.error(f"yt-dlp also failed: {str(e2)}")
                raise InvalidSearchQueryError("All search methods failed")

        # Sort results
        if sort == "engagement":
            creators_data.sort(key=lambda x: x.get("engagement", 0), reverse=True)
        elif sort == "followers":
            creators_data.sort(key=lambda x: x.get("followers_raw", 0), reverse=True)

        # Convert to Creator models
        creators = []
        for data in creators_data[:limit]:
            logger.info(f"DEBUG data type: {type(data)} value: {str(data)[:100]}")
            # Calculate scores
            recent_videos = await youtube_service.get_recent_videos(data.get("id", ""), max_results=10)
            upload_dates = [v["published_at"][:10] for v in recent_videos if isinstance(v, dict) and v.get("published_at")]
            consistency_score = scoring_service.calculate_upload_consistency(upload_dates)
            engagement_rate = data.get("engagement", 0.0)
            campaign_ready = scoring_service.calculate_campaign_readiness(
                consistency_score, engagement_rate
            )
            logger.info(f"DEBUG before ai_summary")
            ai_summary = scoring_service.generate_ai_summary(data)
            logger.info(f"DEBUG before why_recommended")
            why_recommended = scoring_service.generate_why_recommended(
                data, {"consistency_score": consistency_score}
            )
            logger.info(f"DEBUG before Creator()")
            creator = Creator(
                id=data.get("id", ""),
                name=data.get("name", ""),
                handle=data.get("handle", ""),
                avatar=data.get("thumbnail", ""),
                platform=data.get("platform", "youtube"),
                followers=data.get("followers", "0"),
                engagement=float(engagement_rate),
                engagementTrend="up",
                uploadConsistency=consistency_score,
                campaignReady=campaign_ready,
                niche=data.get("niche", "Varied"),
                aiSummary=ai_summary,
                whyRecommended=why_recommended,
                recentPosts=len(upload_dates),
                avgViews=data.get("views", "0"),
            )
            creators.append(creator)

        result = CreatorSearchResponse(
            creators=creators,
            total=len(creators),
            source=source,
            fallback_used=fallback_used,
        )

        # Cache result
        cache.set(cache_key, result, ttl=3600)

        return result

    except InvalidSearchQueryError:
        raise
    except Exception as e:
        logger.error(f"Search error: {str(e)}")
        raise InvalidSearchQueryError(f"Search failed: {str(e)}")


@router.get("/{creator_id}", response_model=Creator)
async def get_creator(creator_id: str) -> Creator:
    """Get creator by ID.

    Args:
        creator_id: Creator ID

    Returns:
        Creator object

    Raises:
        CreatorNotFoundError: If creator not found
    """
    try:
        # This would query database in production
        # For now, return mock data
        logger.info(f"Getting creator: {creator_id}")

        creator = Creator(
            id=creator_id,
            name="Sample Creator",
            handle="@samplecreator",
            platform="youtube",
            followers="1.1M",
            engagement=6.2,
            uploadConsistency=88,
            campaignReady="ready",
            niche="Tech",
            aiSummary="Sample creator profile.",
            whyRecommended="Good metrics overall.",
            recentPosts=12,
            avgViews="420K",
        )

        return creator

    except Exception as e:
        logger.error(f"Get creator error: {str(e)}")
        raise CreatorNotFoundError(creator_id)


@router.get("/{creator_id}/audit", response_model=AuditResult)
async def audit_creator(creator_id: str) -> AuditResult:
    """Audit a creator.

    Args:
        creator_id: Creator ID

    Returns:
        Audit result
    """
    logger.info(f"Auditing creator: {creator_id}")

    return AuditResult(
        creator_id=creator_id,
        upload_history=[],
        consistency_trend="stable",
        engagement_trend=[4.5, 5.0, 5.2, 5.1, 4.9],
        risk_flags=[],
        last_audit_date="2026-05-14T00:00:00Z",
    )
