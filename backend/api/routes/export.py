"""Export routes."""
from fastapi import APIRouter, Query, Path, HTTPException
from fastapi.responses import StreamingResponse
from typing import List, Dict, Any
import io
from datetime import datetime, timedelta

from models.schemas import Creator, ExportRequest, ExportResponse
from services.export_service import ExportService
from core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/export", tags=["export"])

export_service = ExportService()

# In-memory export store (will be replaced by database in production)
export_store: Dict[str, Dict[str, Any]] = {}


@router.post("/{format_type}", response_model=ExportResponse)
async def create_export(
    format_type: str = Path(..., regex="^(csv|json|pdf)$"),
    creator_ids: List[str] = Query(default=[]),
) -> ExportResponse:
    """Create an export request.

    Args:
        format_type: Export format (csv|json|pdf)
        creator_ids: Creator IDs to export (empty = demo/all creators)

    Returns:
        Export response with download URL
    """
    try:
        logger.info(f"Creating {format_type} export for {len(creator_ids) if creator_ids else 'demo'} creators")

        # Generate mock creators for demo/all export
        creators = _get_demo_creators()

        logger.info(f"Exporting {len(creators)} creators in {format_type} format")

        # Generate file content
        if format_type == "csv":
            content = export_service.export_to_csv(creators)
            filename = "creators_export.csv"
            media_type = "text/csv"
        elif format_type == "json":
            content = export_service.export_to_json(creators)
            filename = "creators_export.json"
            media_type = "application/json"
        else:  # pdf
            content = export_service.export_to_pdf(creators)
            filename = "creators_export.html"
            media_type = "text/html"

        # Store export data
        export_id = f"export_{int(datetime.utcnow().timestamp() * 1000)}"
        export_store[export_id] = {
            "format": format_type,
            "content": content,
            "media_type": media_type,
            "filename": filename,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(hours=24)).isoformat(),
        }

        logger.info(f"Export created: {export_id} ({format_type}, {len(content)} bytes)")

        return ExportResponse(
            export_id=export_id,
            download_url=f"/api/export/{export_id}/download",
            expires_at=(datetime.utcnow() + timedelta(hours=24)).isoformat(),
            status="ready",
        )

    except Exception as e:
        logger.error(f"Export creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")


@router.get("/{export_id}/download")
async def download_export(export_id: str):
    """Download an export file.

    Args:
        export_id: Export ID

    Returns:
        Streamed file
    """
    try:
        logger.info(f"Downloading export: {export_id}")

        if export_id not in export_store:
            logger.warning(f"Export not found: {export_id}")
            raise HTTPException(status_code=404, detail="Export not found or expired")

        export_data = export_store[export_id]

        # Check expiration
        expires_at = datetime.fromisoformat(export_data["expires_at"])
        if datetime.utcnow() > expires_at:
            del export_store[export_id]
            raise HTTPException(status_code=410, detail="Export expired")

        # Stream the file
        content = export_data["content"]
        media_type = export_data["media_type"]
        filename = export_data["filename"]

        logger.info(f"Streaming export: {export_id} ({len(content)} bytes)")

        return StreamingResponse(
            iter([content]),
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


def _get_demo_creators() -> List[Creator]:
    """Get demo creators for export.

    Returns:
        List of Creator objects
    """
    return [
        Creator(
            id="1",
            name="Maya Rodriguez",
            handle="@mayacreates",
            platform="instagram",
            followers="2.3M",
            engagement=4.8,
            engagementTrend="up",
            uploadConsistency=92,
            campaignReady="ready",
            niche="Lifestyle",
            aiSummary="High-performing lifestyle creator with consistent brand partnerships. Strong audience in 18-34 demo. Excellent story completion rates and saved-post ratios.",
            whyRecommended="Top 3% engagement in lifestyle category. Previous brand collabs with similar products saw 2.4x ROAS.",
            recentPosts=24,
            avgViews="890K",
        ),
        Creator(
            id="2",
            name="Kai Nakamura",
            handle="@kaitech",
            platform="youtube",
            followers="1.1M",
            engagement=6.2,
            engagementTrend="up",
            uploadConsistency=88,
            campaignReady="ready",
            niche="Tech",
            aiSummary="Trusted tech reviewer with deep audience trust signals. Comment sentiment analysis shows 94% positive. High watch-time retention at 68% avg.",
            whyRecommended="Audience overlap with target demo is 78%. Previous sponsored content outperformed channel average by 1.8x.",
            recentPosts=12,
            avgViews="420K",
        ),
        Creator(
            id="3",
            name="Aria Chen",
            handle="@ariastyle",
            platform="tiktok",
            followers="4.7M",
            engagement=8.1,
            engagementTrend="up",
            uploadConsistency=95,
            campaignReady="ready",
            niche="Fashion",
            aiSummary="Top-tier fashion content creator with viral potential. Audience skews 65% female, 18-28, high disposable income. Aesthetic alignment with premium brands.",
            whyRecommended="Highest engagement rate in dataset. Recent fashion collab content achieved 12M views. Perfect fit for luxury campaigns.",
            recentPosts=47,
            avgViews="2.1M",
        ),
        Creator(
            id="4",
            name="Alex Thompson",
            handle="@fitnessguru",
            platform="instagram",
            followers="890K",
            engagement=5.3,
            engagementTrend="down",
            uploadConsistency=78,
            campaignReady="review",
            niche="Fitness",
            aiSummary="Growing fitness content creator with passionate community. Engagement trending down slightly but still strong. Audience demographics ideal for fitness brands.",
            whyRecommended="Good audience fit for fitness category. Recent workout content averaged 156K views.",
            recentPosts=18,
            avgViews="156K",
        ),
    ]

