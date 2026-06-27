"""Unified feed request and response schemas."""

from enum import Enum

from pydantic import BaseModel, Field

from app.models.asset import AssetType
from app.schemas.asset import AssetResponse
from app.schemas.project import ProjectResponse


class FeedTrack(str, Enum):
    """Which dashboard track(s) to include in the unified feed."""

    ALL = "all"
    PROJECTS = "projects"
    ASSETS = "assets"


class UnifiedFeedResponse(BaseModel):
    """Combined pipeline + asset grid response."""

    track: FeedTrack
    projects: list[ProjectResponse] = Field(default_factory=list)
    assets: list[AssetResponse] = Field(default_factory=list)
    total_projects: int = 0
    total_assets: int = 0
    filters_applied: dict = Field(default_factory=dict)
