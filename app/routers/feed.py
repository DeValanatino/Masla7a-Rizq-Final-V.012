"""
Unified feed routes.

GET /feed/unified — combined pipeline + asset grid, subscription-gated.
"""

from fastapi import APIRouter, Depends, Query

from app.config import DEFAULT_FEED_LIMIT
from app.dependencies.subscription import require_active_subscription
from app.models.asset import AssetType
from app.models.user import User
from app.schemas.feed import FeedTrack, UnifiedFeedResponse
from app.services.feed_service import FeedService


router = APIRouter(prefix="/feed", tags=["Unified Dashboard"])


def _get_feed_service() -> FeedService:
    from app.main import asset_repo, project_repo
    return FeedService(project_repo=project_repo, asset_repo=asset_repo)


@router.get(
    "/unified",
    response_model=UnifiedFeedResponse,
    summary="Unified marketplace feed (subscription required)",
    description=(
        "Returns active project pipelines and available asset listings in one response. "
        "Protected by the 200 EGP subscription gatekeeper — expired users receive HTTP 402."
    ),
    responses={
        402: {
            "description": "Subscription expired — unified feed locked",
            "content": {
                "application/json": {
                    "example": {
                        "detail": {
                            "locked": True,
                            "message_en": "Your Msla7a Rizq subscription has expired. Renew for 200 EGP to unlock the unified feed.",
                            "renewal_required": True,
                        }
                    }
                }
            },
        },
    },
)
def get_unified_feed(
    track: FeedTrack = Query(
        default=FeedTrack.ALL,
        description="Filter by dashboard track: all, projects, or assets",
    ),
    stage_name: str | None = Query(
        default=None,
        description="Filter projects containing this stage name",
    ),
    asset_type: AssetType | None = Query(
        default=None,
        description="Filter assets by type",
    ),
    only_open_stages: bool = Query(
        default=False,
        description="When true, only show projects with Pending/Active stages",
    ),
    only_available_assets: bool = Query(
        default=True,
        description="When true, only show Available assets",
    ),
    limit: int = Query(
        default=DEFAULT_FEED_LIMIT,
        ge=1,
        le=100,
        description="Max items per track",
    ),
    current_user: User = Depends(require_active_subscription),
    feed_service: FeedService = Depends(_get_feed_service),
) -> UnifiedFeedResponse:
    """
    Single unified endpoint for both marketplace tracks.

    Requires an active 200 EGP subscription (The Gatekeeper).
    """
    return feed_service.get_unified_feed(
        user=current_user,
        track=track,
        stage_name=stage_name,
        asset_type=asset_type,
        only_open_stages=only_open_stages,
        only_available_assets=only_available_assets,
        limit=limit,
    )
