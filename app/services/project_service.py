"""
Project pipeline service.

Any authenticated user may create a project — no role-based lock.
Account type (Factory, Workshop, etc.) is informational only.
"""

from app.models.project import Project, ProjectStage, StageStatus
from app.models.user import User
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import CreateProjectRequest, ProjectResponse, StageResponse


class ProjectService:
    """Business logic for the pipeline track."""

    def __init__(self, project_repo: ProjectRepository) -> None:
        self._projects = project_repo

    def create_project(
        self,
        creator: User,
        payload: CreateProjectRequest,
    ) -> ProjectResponse:
        """
        Create a multi-stage manufacturing pipeline.

        The first stage is automatically marked Active if none are specified
        as active, ensuring the pipeline always has a clear entry point.
        """
        stages = [
            ProjectStage(
                name=s.name,
                status=s.status,
                worker_id=s.worker_id,
            )
            for s in payload.stages
        ]

        # Auto-activate the first stage when no stage is explicitly Active
        if not any(s.status == StageStatus.ACTIVE for s in stages):
            stages[0].status = StageStatus.ACTIVE

        project = Project(
            creator_id=creator.id,
            title=payload.title,
            description=payload.description,
            stages=stages,
        )
        saved = self._projects.save(project)
        return self._to_response(saved)

    @staticmethod
    def _to_response(project: Project) -> ProjectResponse:
        """Map domain model to API response schema."""
        return ProjectResponse(
            id=project.id,
            creator_id=project.creator_id,
            title=project.title,
            description=project.description,
            stages=[
                StageResponse(
                    name=s.name,
                    status=s.status,
                    worker_id=s.worker_id,
                )
                for s in project.stages
            ],
            created_at=project.created_at.isoformat(),
            is_active=project.is_active,
        )
