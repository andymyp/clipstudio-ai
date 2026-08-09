"""Candidate deduplication ports and exact URL/content checks."""

from typing import Protocol

from .schemas import DuplicateMatch, VideoMetadata


class SemanticDeduplicator(Protocol):
    """Replaceable semantic similarity interface; no vector database is assumed."""

    async def check(self, metadata: VideoMetadata) -> DuplicateMatch:
        """Return a semantic duplicate decision."""


class NoopSemanticDeduplicator:
    """Default semantic port that never rejects a candidate."""

    async def check(self, metadata: VideoMetadata) -> DuplicateMatch:
        """Return an undecided semantic result."""
        return DuplicateMatch(duplicate=False)
