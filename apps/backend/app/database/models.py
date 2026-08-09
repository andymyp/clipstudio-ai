"""SQLAlchemy metadata models for the ClipStudio AI operational store."""

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import (
    JSON,
    DateTime,
    Float,
    ForeignKey,
    Index,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


def new_id() -> str:
    """Generate a portable, opaque entity identifier."""
    return str(uuid4())


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(UTC)


class EntityMixin:
    """Common identity and UTC audit fields."""

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, onupdate=utc_now
    )


class Agent(EntityMixin, Base):
    """Persisted autonomous-agent definition."""

    __tablename__ = "agents"
    __table_args__ = (Index("ix_agents_status", "status"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="inactive")
    configuration: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    schedule: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    watermark: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    config: Mapped["AgentConfig | None"] = relationship(
        back_populates="agent", uselist=False
    )
    video_sources: Mapped[list["VideoSource"]] = relationship(back_populates="agent")
    workflows: Mapped[list["Workflow"]] = relationship(back_populates="agent")
    clips: Mapped[list["Clip"]] = relationship(back_populates="agent")


class AgentConfig(EntityMixin, Base):
    """Versionable agent behavior configuration."""

    __tablename__ = "agent_configs"
    __table_args__ = (UniqueConstraint("agent_id", name="uq_agent_configs_agent_id"),)

    agent_id: Mapped[str] = mapped_column(
        ForeignKey("agents.id", ondelete="CASCADE"), nullable=False
    )
    sources: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    prompt: Mapped[str | None] = mapped_column(Text)
    model_settings: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )
    scoring_rules: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    agent: Mapped[Agent] = relationship(back_populates="config")


class VideoSource(EntityMixin, Base):
    """Discovered source-video metadata; media remains on the filesystem."""

    __tablename__ = "video_sources"
    __table_args__ = (
        Index("ix_video_sources_agent_id", "agent_id"),
        Index("ix_video_sources_content_hash", "content_hash"),
        UniqueConstraint("url", name="uq_video_sources_url"),
    )

    agent_id: Mapped[str | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL")
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    platform: Mapped[str] = mapped_column(String(80), nullable=False)
    title: Mapped[str | None] = mapped_column(String(500))
    duration: Mapped[float | None] = mapped_column(Float)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )
    content_hash: Mapped[str | None] = mapped_column(String(128), unique=True)
    status: Mapped[str] = mapped_column(
        String(40), nullable=False, default="discovered"
    )

    agent: Mapped[Agent | None] = relationship(back_populates="video_sources")
    transcripts: Mapped[list["Transcript"]] = relationship(
        back_populates="video_source"
    )
    analyses: Mapped[list["VideoAnalysis"]] = relationship(
        back_populates="video_source"
    )
    clips: Mapped[list["Clip"]] = relationship(back_populates="source_video")


class Transcript(EntityMixin, Base):
    """Transcript output with timestamped segment data."""

    __tablename__ = "transcripts"
    __table_args__ = (Index("ix_transcripts_video_id", "video_id"),)

    video_id: Mapped[str] = mapped_column(
        ForeignKey("video_sources.id", ondelete="CASCADE"), nullable=False
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    segments: Mapped[list[Any]] = mapped_column(JSON, default=list, nullable=False)
    language: Mapped[str | None] = mapped_column(String(16))
    timestamps: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    video_source: Mapped[VideoSource] = relationship(back_populates="transcripts")


class VideoAnalysis(EntityMixin, Base):
    """Structured analysis scores and model output for a source video."""

    __tablename__ = "video_analysis"
    __table_args__ = (Index("ix_video_analysis_video_id", "video_id"),)

    video_id: Mapped[str] = mapped_column(
        ForeignKey("video_sources.id", ondelete="CASCADE"), nullable=False
    )
    emotion_score: Mapped[float | None] = mapped_column(Float)
    hook_score: Mapped[float | None] = mapped_column(Float)
    quality_score: Mapped[float | None] = mapped_column(Float)
    ai_result: Mapped[dict[str, Any]] = mapped_column(
        JSON, default=dict, nullable=False
    )

    video_source: Mapped[VideoSource] = relationship(back_populates="analyses")


class Workflow(EntityMixin, Base):
    """Workflow execution state owned by the future orchestration layer."""

    __tablename__ = "workflows"
    __table_args__ = (Index("ix_workflows_status", "status"),)

    agent_id: Mapped[str | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL")
    )
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending")
    current_step: Mapped[str | None] = mapped_column(String(100))
    progress: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    agent: Mapped[Agent | None] = relationship(back_populates="workflows")
    tasks: Mapped[list["WorkflowTask"]] = relationship(back_populates="workflow")


class WorkflowTask(EntityMixin, Base):
    """Individual resumable task state within a workflow."""

    __tablename__ = "workflow_tasks"
    __table_args__ = (Index("ix_workflow_tasks_status", "status"),)

    workflow_id: Mapped[str] = mapped_column(
        ForeignKey("workflows.id", ondelete="CASCADE"), nullable=False
    )
    task_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending")
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON)
    error: Mapped[str | None] = mapped_column(Text)

    workflow: Mapped[Workflow] = relationship(back_populates="tasks")


class Clip(EntityMixin, Base):
    """Generated clip metadata and review status."""

    __tablename__ = "clips"
    __table_args__ = (Index("ix_clips_status", "status"),)

    source_video_id: Mapped[str] = mapped_column(
        ForeignKey("video_sources.id", ondelete="CASCADE"), nullable=False
    )
    agent_id: Mapped[str | None] = mapped_column(
        ForeignKey("agents.id", ondelete="SET NULL")
    )
    file_path: Mapped[str | None] = mapped_column(String(2048))
    duration: Mapped[float | None] = mapped_column(Float)
    score: Mapped[float | None] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="generated")
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON, default=dict, nullable=False
    )

    source_video: Mapped[VideoSource] = relationship(back_populates="clips")
    agent: Mapped[Agent | None] = relationship(back_populates="clips")
    metadata_record: Mapped["ClipMetadata | None"] = relationship(
        back_populates="clip", uselist=False
    )


class ClipMetadata(EntityMixin, Base):
    """Generated platform-specific posting metadata."""

    __tablename__ = "clip_metadata"
    __table_args__ = (UniqueConstraint("clip_id", name="uq_clip_metadata_clip_id"),)

    clip_id: Mapped[str] = mapped_column(
        ForeignKey("clips.id", ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    hashtags: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)
    platform: Mapped[str | None] = mapped_column(String(80))

    clip: Mapped[Clip] = relationship(back_populates="metadata_record")


class AIModel(EntityMixin, Base):
    """Replaceable AI model registry metadata."""

    __tablename__ = "ai_models"
    __table_args__ = (Index("ix_ai_models_status", "status"),)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    provider: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(80), nullable=False)
    version: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="available")


class ProcessingHistory(EntityMixin, Base):
    """Traceable system actions, events, and structured results."""

    __tablename__ = "processing_history"
    __table_args__ = (
        Index("ix_processing_history_entity", "entity_type", "entity_id"),
    )

    entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    entity_id: Mapped[str | None] = mapped_column(String(36))
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    event: Mapped[str | None] = mapped_column(String(120))
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON)


__all__ = [
    "AIModel",
    "Agent",
    "AgentConfig",
    "Clip",
    "ClipMetadata",
    "EntityMixin",
    "ProcessingHistory",
    "Transcript",
    "VideoAnalysis",
    "VideoSource",
    "Workflow",
    "WorkflowTask",
]
