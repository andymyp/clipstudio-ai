"""Typed workflow definitions, states, and execution results."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class WorkflowState(StrEnum):
    """Persisted workflow lifecycle states."""

    CREATED = "created"
    QUEUED = "queued"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskState(StrEnum):
    """Persisted task lifecycle states."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"
    SKIPPED = "skipped"


class WorkflowTaskDefinition(BaseModel):
    """Independent task definition with explicit dependencies and retry policy."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    task_type: str = Field(min_length=1, max_length=100)
    dependencies: list[str] = Field(default_factory=list)
    input: dict[str, Any] = Field(default_factory=dict)
    max_attempts: int = Field(default=3, ge=1, le=10)
    retry_delay_seconds: float = Field(default=0, ge=0, le=3600)


class WorkflowDefinition(BaseModel):
    """Reusable workflow template or persisted workflow instance definition."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    agent_id: str | None = None
    tasks: list[WorkflowTaskDefinition] = Field(min_length=1, max_length=100)
    max_concurrency: int = Field(default=2, ge=1, le=16)


class TaskResult(BaseModel):
    """Normalized task output with attempt and duration metadata."""

    task_id: str
    task_type: str
    status: TaskState
    output: dict[str, Any] = Field(default_factory=dict)
    attempts: int = Field(ge=1)
    duration_seconds: float = Field(ge=0)
    error: str | None = None


class WorkflowRunResult(BaseModel):
    """Summary returned by one workflow execution."""

    workflow_id: str
    state: WorkflowState
    completed_tasks: int = Field(ge=0)
    total_tasks: int = Field(ge=0)
    progress: float = Field(ge=0, le=100)
    results: list[TaskResult] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
