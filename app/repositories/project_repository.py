"""
In-memory project repository.

Supabase migration path:
  store stages as a JSONB column or a related `project_stages` table.
"""

from app.models.project import Project, StageStatus
from app.repositories.base import BaseRepository


class ProjectRepository(BaseRepository[Project]):
    """In-memory store for pipeline projects."""

    def __init__(self) -> None:
        self._store: dict[str, Project] = {}

    def get_by_id(self, project_id: str) -> Project | None:
        return self._store.get(project_id)

    def save(self, project: Project) -> Project:
        self._store[project.id] = project
        return project

    def list_all(self) -> list[Project]:
        return list(self._store.values())

    def list_active(self) -> list[Project]:
        """Return only active pipeline projects."""
        return [p for p in self._store.values() if p.is_active]

    def filter_by_criteria(
        self,
        *,
        creator_id: str | None = None,
        stage_name: str | None = None,
        has_open_stage: bool | None = None,
        limit: int = 50,
    ) -> list[Project]:
        """
        Dynamic filtering for the unified feed.

        Args:
            creator_id: Restrict to projects owned by a specific user.
            stage_name: Match projects containing a stage with this name.
            has_open_stage: When True, only projects with Pending/Active stages.
            limit: Maximum number of results.
        """
        results = self.list_active()

        if creator_id:
            results = [p for p in results if p.creator_id == creator_id]

        if stage_name:
            needle = stage_name.strip().lower()
            results = [
                p for p in results
                if any(s.name.lower() == needle for s in p.stages)
            ]

        if has_open_stage is True:
            open_statuses = {StageStatus.PENDING, StageStatus.ACTIVE}
            results = [
                p for p in results
                if any(s.status in open_statuses for s in p.stages)
            ]

        results.sort(key=lambda p: p.created_at, reverse=True)
        return results[:limit]
