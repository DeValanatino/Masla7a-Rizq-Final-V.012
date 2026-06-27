"""
Asset sharing domain model.

Mirrors the future Supabase `assets` table for the asset track:
  id, owner_id, asset_type, description, status
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class AssetType(str, Enum):
    """Category of shared industrial asset."""

    MACHINE_SHARING = "Machine Sharing"
    EXCESS_MATERIAL = "Excess Material"


class AssetStatus(str, Enum):
    """Availability state of a listed asset."""

    AVAILABLE = "Available"
    RENTED = "Rented"


@dataclass
class Asset:
    """An idle machine or excess material listed on the asset grid."""

    owner_id: str
    asset_type: AssetType
    description: str
    status: AssetStatus = AssetStatus.AVAILABLE
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "asset_type": self.asset_type.value,
            "description": self.description,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Asset":
        return cls(
            id=data["id"],
            owner_id=data["owner_id"],
            asset_type=AssetType(data["asset_type"]),
            description=data["description"],
            status=AssetStatus(data.get("status", AssetStatus.AVAILABLE.value)),
            created_at=datetime.fromisoformat(data["created_at"]),
        )
