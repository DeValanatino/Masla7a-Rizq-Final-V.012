"""
Asset sharing service.

Any authenticated user may list assets — no fixed role locks.
Account type labels (Factory, Workshop) are profile metadata, not gates.
"""

from app.models.asset import Asset, AssetStatus
from app.models.user import User
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import AssetResponse, ShareAssetRequest


class AssetService:
    """Business logic for the asset track."""

    def __init__(self, asset_repo: AssetRepository) -> None:
        self._assets = asset_repo

    def share_asset(self, owner: User, payload: ShareAssetRequest) -> AssetResponse:
        """
        List an idle machine or excess material on the asset grid.

        All authenticated users can share — the unified dashboard supports
        both tracks regardless of account_type.
        """
        asset = Asset(
            owner_id=owner.id,
            asset_type=payload.asset_type,
            description=payload.description,
            status=AssetStatus.AVAILABLE,
        )
        saved = self._assets.save(asset)
        return self._to_response(saved)

    @staticmethod
    def _to_response(asset: Asset) -> AssetResponse:
        """Map domain model to API response schema."""
        return AssetResponse(
            id=asset.id,
            owner_id=asset.owner_id,
            asset_type=asset.asset_type,
            description=asset.description,
            status=asset.status,
            created_at=asset.created_at.isoformat(),
        )
