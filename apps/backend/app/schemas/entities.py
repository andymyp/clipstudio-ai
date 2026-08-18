"""Validated input contracts for database-backed entities."""

from typing import Any

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class AgentCreate(BaseModel):
    """Validated agent definition input."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    configuration: dict[str, Any] = Field(default_factory=dict)
    schedule: dict[str, Any] = Field(default_factory=dict)
    watermark: dict[str, Any] = Field(default_factory=dict)


class VideoSourceCreate(BaseModel):
    """Validated discovered-source input."""

    model_config = ConfigDict(extra="forbid")

    url: AnyHttpUrl
    platform: str = Field(min_length=1, max_length=80)
    title: str | None = Field(default=None, max_length=500)
    duration: float | None = Field(default=None, ge=0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class WorkflowCreate(BaseModel):
    """Validated workflow input."""

    model_config = ConfigDict(extra="forbid")

    agent_id: str | None = None
    current_step: str | None = Field(default=None, max_length=100)


class ClipCreate(BaseModel):
    """Validated generated-clip metadata input."""

    model_config = ConfigDict(extra="forbid")

    source_video_id: str
    agent_id: str | None = None
    file_path: str | None = Field(default=None, max_length=2048)
    duration: float | None = Field(default=None, ge=0)
    score: float | None = Field(default=None, ge=0, le=100)
