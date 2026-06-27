"""Asset sharing request and response schemas."""

from pydantic import BaseModel, Field

from app.models.asset import AssetStatus, AssetType


class ShareAssetRequest(BaseModel):
    """Payload for listing an idle machine or excess material."""

    asset_type: AssetType
    description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        examples=["Idle CNC machine available for 3 days"],
    )


class AssetResponse(BaseModel):
    """Serialized asset listing."""

    id: str
    owner_id: str
    asset_type: AssetType
    description: str
    status: AssetStatus
    created_at: str
