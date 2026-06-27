"""Project pipeline request and response schemas."""

from pydantic import BaseModel, Field

from app.models.project import StageStatus


class StageInput(BaseModel):
    """Input for one sequential manufacturing stage."""

    name: str = Field(..., min_length=2, max_length=100, examples=["CNC Cutting"])
    status: StageStatus = StageStatus.PENDING
    worker_id: str | None = None


class CreateProjectRequest(BaseModel):
    """Payload for posting a multi-stage manufacturing pipeline."""

    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    stages: list[StageInput] = Field(
        ...,
        min_length=1,
        description="Ordered list of sequential manufacturing stages",
        examples=[[
            {"name": "CNC Cutting"},
            {"name": "Carpentry Assembly"},
            {"name": "Spray Painting"},
            {"name": "Truck Logistics"},
        ]],
    )


class StageResponse(BaseModel):
    """Serialized project stage."""

    name: str
    status: StageStatus
    worker_id: str | None


class ProjectResponse(BaseModel):
    """Serialized project pipeline."""

    id: str
    creator_id: str
    title: str
    description: str
    stages: list[StageResponse]
    created_at: str
    is_active: bool
