"""REST API request and response contracts."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .entities import AgentCreate, ClipCreate, VideoSourceCreate, WorkflowCreate


class Page[DataT](BaseModel):
    """Bounded collection response with pagination metadata."""

    items: list[DataT]
    limit: int
    offset: int
    returned: int


class AgentResponse(AgentCreate):
    """Public agent representation."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    status: str
    created_at: datetime
    updated_at: datetime


class AgentUpdate(BaseModel):
    """Partial mutable agent fields."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=200)
    category: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    configuration: dict[str, Any] | None = None
    schedule: dict[str, Any] | None = None
    watermark: dict[str, Any] | None = None


class VideoResponse(VideoSourceCreate):
    """Public video-source representation."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="ignore"
    )

    id: str
    agent_id: str | None
    status: str
    content_hash: str | None
    created_at: datetime
    updated_at: datetime
    metadata: dict[str, Any] = Field(
        default_factory=dict, validation_alias="metadata_json"
    )


class WorkflowResponse(WorkflowCreate):
    """Public workflow status representation."""

    model_config = ConfigDict(from_attributes=True, extra="ignore")

    id: str
    status: str
    progress: float
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime
    errors: list[str] = Field(default_factory=list)
    duration_seconds: float | None = None


class ClipResponse(ClipCreate):
    """Public clip representation."""

    model_config = ConfigDict(
        from_attributes=True, populate_by_name=True, extra="ignore"
    )

    id: str
    status: str
    metadata: dict[str, Any] = Field(
        default_factory=dict, validation_alias="metadata_json"
    )
    created_at: datetime
    updated_at: datetime


class ModelResponse(BaseModel):
    """Public model registry representation."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    provider: str
    type: str
    version: str
    status: str
    created_at: datetime
    updated_at: datetime


class SettingsUpdate(BaseModel):
    """Safe mutable runtime settings; secrets are intentionally absent."""

    model_config = ConfigDict(extra="forbid")

    debug: bool | None = None
    log_level: str | None = Field(
        default=None, pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$"
    )
    host: str | None = Field(default=None, min_length=1, max_length=255)
    port: int | None = Field(default=None, ge=1, le=65535)


class JobResponse(BaseModel):
    """Accepted asynchronous operation response."""

    job_id: str
    status: str = "queued"
