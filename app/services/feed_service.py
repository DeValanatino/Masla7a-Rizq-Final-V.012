"""
Unified feed service.

Merges active project pipelines and available asset listings into a single
dashboard response, filtered by the caller's target criteria.
"""

from app.config import DEFAULT_FEED_LIMIT
from app.models.asset import AssetStatus, AssetType
from app.models.user import User
from app.repositories.asset_repository import AssetRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.asset import AssetResponse
from app.schemas.feed import FeedTrack, UnifiedFeedResponse
from app.schemas.project import ProjectResponse
from app.services.asset_service import AssetService
from app.services.project_service import ProjectService


class FeedService:
    """Aggregates both dashboard tracks with dynamic filtering."""

    def __init__(
        self,
        project_repo: ProjectRepository,
        asset_repo: AssetRepository,
    ) -> None:
        self._projects = project_repo
        self._assets = asset_repo

    def get_unified_feed(
        self,
        user: User,
        *,
        track: FeedTrack = FeedTrack.ALL,
        stage_name: str | None = None,
        asset_type: AssetType | None = None,
        only_open_stages: bool = False,
        only_available_assets: bool = True,
        limit: int = DEFAULT_FEED_LIMIT,
    ) -> UnifiedFeedResponse:
        """
        Build the unified dashboard feed.

        Filter parameters let each user narrow results to their target criteria
        without switching between separate endpoints.
        """
        filters_applied: dict = {"track": track.value, "limit": limit}

        project_items: list[ProjectResponse] = []
        asset_items: list[AssetResponse] = []

        if track in (FeedTrack.ALL, FeedTrack.PROJECTS):
            if stage_name:
                filters_applied["stage_name"] = stage_name
            if only_open_stages:
                filters_applied["only_open_stages"] = True

            raw_projects = self._projects.filter_by_criteria(
                stage_name=stage_name,
                has_open_stage=only_open_stages if only_open_stages else None,
                limit=limit,
            )
            project_items = [
                ProjectService._to_response(p) for p in raw_projects
            ]

        if track in (FeedTrack.ALL, FeedTrack.ASSETS):
            if asset_type:
                filters_applied["asset_type"] = asset_type.value
            if only_available_assets:
                filters_applied["only_available_assets"] = True

            raw_assets = self._assets.filter_by_criteria(
                asset_type=asset_type,
                status=AssetStatus.AVAILABLE if only_available_assets else None,
                limit=limit,
            )
            asset_items = [
                AssetService._to_response(a) for a in raw_assets
            ]

        return UnifiedFeedResponse(
            track=track,
            projects=project_items,
            assets=asset_items,
            total_projects=len(project_items),
            total_assets=len(asset_items),
            filters_applied=filters_applied,
        )
