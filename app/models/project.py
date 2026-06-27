"""
Project pipeline domain model.

Mirrors the future Supabase `projects` table with an embedded stages array.
Each stage tracks its own active status and assigned craftsman worker_id.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class StageStatus(str, Enum):
    """Lifecycle state of an individual manufacturing stage."""

    PENDING = "Pending"
    ACTIVE = "Active"
    COMPLETED = "Completed"


@dataclass
class ProjectStage:
    """One sequential step in a multi-stage manufacturing pipeline."""

    name: str
    status: StageStatus = StageStatus.PENDING
    worker_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "status": self.status.value,
            "worker_id": self.worker_id,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectStage":
        return cls(
            name=data["name"],
            status=StageStatus(data.get("status", StageStatus.PENDING.value)),
            worker_id=data.get("worker_id"),
        )


@dataclass
class Project:
    """A multi-stage manufacturing project posted to the pipeline track."""

    creator_id: str
    title: str
    description: str
    stages: list[ProjectStage]
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

    @property
    def active_stage(self) -> ProjectStage | None:
        """Return the currently active stage, if any."""
        for stage in self.stages:
            if stage.status == StageStatus.ACTIVE:
                return stage
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "title": self.title,
            "description": self.description,
            "stages": [s.to_dict() for s in self.stages],
            "created_at": self.created_at.isoformat(),
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Project":
        return cls(
            id=data["id"],
            creator_id=data["creator_id"],
            title=data["title"],
            description=data["description"],
            stages=[ProjectStage.from_dict(s) for s in data["stages"]],
            created_at=datetime.fromisoformat(data["created_at"]),
            is_active=data.get("is_active", True),
        )
