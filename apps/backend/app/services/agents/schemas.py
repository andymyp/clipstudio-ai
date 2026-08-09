"""Typed contracts shared by the generic agent framework."""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AgentGoal(BaseModel):
    """A goal expressed independently of a specific content pipeline."""

    model_config = ConfigDict(extra="forbid")

    objective: str = Field(min_length=1, max_length=2000)
    constraints: dict[str, Any] = Field(default_factory=dict)
    expected_output: str | None = Field(default=None, max_length=2000)


class AgentConfiguration(BaseModel):
    """Versionable agent configuration and execution policy."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=200)
    category: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=5000)
    goal: AgentGoal
    sources: list[Any] = Field(default_factory=list)
    prompt: str | None = Field(default=None, max_length=10000)
    model: dict[str, Any] = Field(default_factory=dict)
    schedule: dict[str, Any] = Field(default_factory=dict)
    watermark: dict[str, Any] = Field(default_factory=dict)
    scoring_rules: dict[str, Any] = Field(default_factory=dict)
    tools: list[str] = Field(default_factory=list)
    max_steps: int = Field(default=10, ge=1, le=100)


class AgentState(StrEnum):
    """Persisted lifecycle labels used by the runtime and database."""

    CREATED = "created"
    CONFIGURED = "configured"
    INACTIVE = "inactive"
    ACTIVE = "active"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
    DISABLED = "disabled"
    ARCHIVED = "archived"


class AgentObservation(BaseModel):
    """Input context supplied to one decision-loop execution."""

    model_config = ConfigDict(extra="forbid")

    data: dict[str, Any] = Field(default_factory=dict)


class PlanStep(BaseModel):
    """One tool action in a generic agent plan."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)
    tool: str = Field(min_length=1, max_length=100)
    input: dict[str, Any] = Field(default_factory=dict)


class ActionPlan(BaseModel):
    """Planner output before any tool is executed."""

    model_config = ConfigDict(extra="forbid")

    objective: str
    steps: list[PlanStep] = Field(default_factory=list)


class Evaluation(BaseModel):
    """Deterministic execution evaluation awaiting future model evaluators."""

    success: bool
    quality_score: float = Field(ge=0, le=100)
    rationale: str


class AgentMetrics(BaseModel):
    """Counters maintained by one agent runtime."""

    videos_found: int = Field(default=0, ge=0)
    clips_generated: int = Field(default=0, ge=0)
    approved_clips: int = Field(default=0, ge=0)
    rejected_clips: int = Field(default=0, ge=0)
    average_score: float = Field(default=0, ge=0, le=100)
    runs: int = Field(default=0, ge=0)


class AgentMonitor(BaseModel):
    """Safe manager status response for monitoring and API adapters."""

    agent_id: str
    state: str
    active_tasks: int = Field(default=0, ge=0)
    metrics: AgentMetrics


class AgentRunResult(BaseModel):
    """Result returned after a decision loop completes."""

    run_id: str
    plan: ActionPlan
    results: list[dict[str, Any]] = Field(default_factory=list)
    evaluation: Evaluation
