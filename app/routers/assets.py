"""
Asset sharing routes.

POST /assets/share — any authenticated user can list idle assets.
"""

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.asset import AssetResponse, ShareAssetRequest
from app.services.asset_service import AssetService


router = APIRouter(prefix="/assets", tags=["Asset Track"])


def _get_asset_service() -> AssetService:
    from app.main import asset_repo
    return AssetService(asset_repo=asset_repo)


@router.post(
    "/share",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Share an idle machine or excess material",
    description=(
        "List an asset on the marketplace grid. "
        "Open to all authenticated users from the unified dashboard — "
        "account_type is profile metadata, not a permission gate."
    ),
)
def share_asset(
    payload: ShareAssetRequest,
    current_user: User = Depends(get_current_user),
    asset_service: AssetService = Depends(_get_asset_service),
) -> AssetResponse:
    """Post a new asset listing on the asset track."""
    return asset_service.share_asset(owner=current_user, payload=payload)
