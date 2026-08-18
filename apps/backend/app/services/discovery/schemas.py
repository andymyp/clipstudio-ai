"""Typed discovery queries, metadata, candidates, and results."""

from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, Field


class CandidateState(StrEnum):
    """Candidate lifecycle labels."""

    FOUND = "found"
    FILTERED = "filtered"
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    REJECTED = "rejected"


class SearchQuery(BaseModel):
    """Agent-provided discovery query normalized for source connectors."""

    model_config = ConfigDict(extra="forbid")

    keywords: list[str] = Field(default_factory=list, max_length=50)
    category: str | None = Field(default=None, max_length=100)
    topic: str | None = Field(default=None, max_length=200)
    language: str | None = Field(default=None, min_length=2, max_length=16)
    platforms: list[str] = Field(default_factory=list, max_length=20)
    limit: int = Field(default=20, ge=1, le=100)

    def text(self) -> str:
        """Build a platform-neutral search phrase."""
        parts = [*self.keywords, self.category, self.topic]
        return " ".join(part.strip() for part in parts if part and part.strip())


class VideoMetadata(BaseModel):
    """Normalized metadata collected without downloading media bytes."""

    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=500)
    description: str | None = Field(default=None, max_length=10000)
    author: str | None = Field(default=None, max_length=300)
    platform: str = Field(min_length=1, max_length=80)
    url: AnyHttpUrl
    duration: float | None = Field(default=None, ge=0)
    published_at: datetime | None = None
    view_count: int = Field(default=0, ge=0)
    like_count: int = Field(default=0, ge=0)
    tags: list[str] = Field(default_factory=list, max_length=100)
    thumbnail_url: AnyHttpUrl | None = None
    language: str | None = Field(default=None, max_length=16)
    content_hash: str | None = Field(default=None, max_length=128)
    quality_score: float | None = Field(default=None, ge=0, le=100)
    extra: dict[str, Any] = Field(default_factory=dict)


class DiscoveryFilters(BaseModel):
    """Cheap pre-download filtering rules."""

    model_config = ConfigDict(extra="forbid")

    min_duration: float | None = Field(default=None, ge=0)
    max_duration: float | None = Field(default=None, ge=0)
    language: str | None = Field(default=None, max_length=16)
    min_quality_score: float | None = Field(default=None, ge=0, le=100)
    min_view_count: int | None = Field(default=None, ge=0)


class DiscoveryCandidate(BaseModel):
    """A normalized source candidate and its current discovery decision."""

    metadata: VideoMetadata
    state: CandidateState = CandidateState.FOUND
    score: float = Field(default=0, ge=0, le=100)
    duplicate: bool = False
    reason: str | None = None
    video_id: str | None = None


class DiscoveryResult(BaseModel):
    """Summary returned by one discovery run."""

    query_id: str
    candidates: list[DiscoveryCandidate] = Field(default_factory=list)
    found_count: int = Field(default=0, ge=0)
    filtered_count: int = Field(default=0, ge=0)
    errors: list[str] = Field(default_factory=list)


class DuplicateMatch(BaseModel):
    """Deduplication decision with a replaceable similarity layer."""

    duplicate: bool
    reason: str | None = None
    similarity: float | None = Field(default=None, ge=0, le=100)
