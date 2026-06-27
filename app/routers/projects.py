"""
Project pipeline routes.

POST /projects/create — any authenticated user can post a pipeline.
"""

from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.project import CreateProjectRequest, ProjectResponse
from app.services.project_service import ProjectService


router = APIRouter(prefix="/projects", tags=["Pipeline Track"])


def _get_project_service() -> ProjectService:
    from app.main import project_repo
    return ProjectService(project_repo=project_repo)


@router.post(
    "/create",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a multi-stage manufacturing project",
    description=(
        "Post a sequential manufacturing pipeline. "
        "Open to all authenticated users — no role-based restrictions."
    ),
)
def create_project(
    payload: CreateProjectRequest,
    current_user: User = Depends(get_current_user),
    project_service: ProjectService = Depends(_get_project_service),
) -> ProjectResponse:
    """Create a new project on the pipeline track."""
    return project_service.create_project(creator=current_user, payload=payload)
