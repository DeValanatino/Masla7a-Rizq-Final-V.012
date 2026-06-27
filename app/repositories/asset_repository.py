"""
In-memory asset repository.

Supabase migration path:
  map directly to an `assets` table with status and asset_type enums.
"""

from app.models.asset import Asset, AssetStatus, AssetType
from app.repositories.base import BaseRepository


class AssetRepository(BaseRepository[Asset]):
    """In-memory store for shared industrial assets."""

    def __init__(self) -> None:
        self._store: dict[str, Asset] = {}

    def get_by_id(self, asset_id: str) -> Asset | None:
        return self._store.get(asset_id)

    def save(self, asset: Asset) -> Asset:
        self._store[asset.id] = asset
        return asset

    def list_all(self) -> list[Asset]:
        return list(self._store.values())

    def filter_by_criteria(
        self,
        *,
        owner_id: str | None = None,
        asset_type: AssetType | None = None,
        status: AssetStatus | None = AssetStatus.AVAILABLE,
        limit: int = 50,
    ) -> list[Asset]:
        """
        Dynamic filtering for the unified feed asset track.

        Args:
            owner_id: Restrict to assets owned by a specific user.
            asset_type: Filter by Machine Sharing or Excess Material.
            status: Default Available — only show rentable items.
            limit: Maximum number of results.
        """
        results = list(self._store.values())

        if owner_id:
            results = [a for a in results if a.owner_id == owner_id]

        if asset_type:
            results = [a for a in results if a.asset_type == asset_type]

        if status:
            results = [a for a in results if a.status == status]

        results.sort(key=lambda a: a.created_at, reverse=True)
        return results[:limit]
