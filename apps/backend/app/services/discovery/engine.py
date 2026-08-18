"""Metadata-first discovery engine with duplicate-safe persistence."""

import asyncio
from collections.abc import Sequence
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from ...core.events import (
    DiscoveryCompleted,
    DiscoveryStarted,
    DuplicateDetected,
    EventBus,
    VideoFiltered,
    VideoFound,
)
from ...database.models import ProcessingHistory, VideoSource
from ...repositories.videos import VideoRepository
from .candidates import NoopSemanticDeduplicator, SemanticDeduplicator
from .connectors import ConnectorError, ConnectorRegistry, default_connector_registry
from .filters import filter_reason, rank_score
from .normalizer import normalize_metadata
from .schemas import (
    CandidateState,
    DiscoveryCandidate,
    DiscoveryFilters,
    DiscoveryResult,
    DuplicateMatch,
    SearchQuery,
    VideoMetadata,
)


class DiscoveryEngine:
    """Search connectors, normalize metadata, filter, deduplicate, and store."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        event_bus: EventBus,
        connectors: ConnectorRegistry | None = None,
        semantic_deduplicator: SemanticDeduplicator | None = None,
        request_delay_seconds: float = 0,
    ) -> None:
        if request_delay_seconds < 0:
            raise ValueError("request delay cannot be negative")
        self.session = session
        self.event_bus = event_bus
        self.connectors = connectors or default_connector_registry()
        self.semantic_deduplicator = semantic_deduplicator or NoopSemanticDeduplicator()
        self.request_delay_seconds = request_delay_seconds

    async def _duplicate_match(self, metadata: VideoMetadata) -> DuplicateMatch:
        """Run cheap URL/content checks before the semantic extension point."""
        repository = VideoRepository(self.session)
        if await repository.get_by_url(str(metadata.url)):
            return DuplicateMatch(
                duplicate=True, reason="duplicate_url", similarity=100
            )
        if metadata.content_hash and await repository.get_by_content_hash(
            metadata.content_hash
        ):
            return DuplicateMatch(
                duplicate=True, reason="duplicate_content_hash", similarity=100
            )
        return await self.semantic_deduplicator.check(metadata)

    async def discover(
        self,
        query: SearchQuery,
        *,
        filters: DiscoveryFilters | None = None,
        agent_id: str | None = None,
        query_id: str | None = None,
    ) -> DiscoveryResult:
        """Execute one asynchronous metadata-only discovery run."""
        run_id = query_id or str(uuid4())
        rules = filters or DiscoveryFilters()
        candidates: list[DiscoveryCandidate] = []
        errors: list[str] = []
        found_count = 0
        filtered_count = 0
        await self.event_bus.publish(DiscoveryStarted(query_id=run_id))
        for connector in self.connectors.select(query.platforms):
            try:
                items: Sequence[VideoMetadata] = await connector.search(query)
                for raw in items[: query.limit]:
                    if self.request_delay_seconds:
                        await asyncio.sleep(self.request_delay_seconds)
                    metadata = normalize_metadata(raw)
                    candidate = DiscoveryCandidate(
                        metadata=metadata,
                        score=rank_score(metadata, query.text()),
                    )
                    duplicate = await self._duplicate_match(metadata)
                    if duplicate.duplicate:
                        candidate.state = CandidateState.REJECTED
                        candidate.duplicate = True
                        candidate.reason = duplicate.reason or "duplicate"
                        filtered_count += 1
                        await self.event_bus.publish(
                            DuplicateDetected(
                                query_id=run_id,
                                platform=metadata.platform,
                                url=str(metadata.url),
                                reason=candidate.reason,
                            )
                        )
                        await self.event_bus.publish(
                            VideoFiltered(
                                query_id=run_id,
                                platform=metadata.platform,
                                url=str(metadata.url),
                                reason=candidate.reason,
                            )
                        )
                        candidates.append(candidate)
                        continue
                    reason = filter_reason(metadata, rules)
                    if reason:
                        candidate.state = CandidateState.FILTERED
                        candidate.reason = reason
                        filtered_count += 1
                        await self.event_bus.publish(
                            VideoFiltered(
                                query_id=run_id,
                                platform=metadata.platform,
                                url=str(metadata.url),
                                reason=reason,
                            )
                        )
                        candidates.append(candidate)
                        continue
                    video = await VideoRepository(self.session).create(
                        VideoSource(
                            agent_id=agent_id,
                            url=str(metadata.url),
                            platform=metadata.platform,
                            title=metadata.title,
                            duration=metadata.duration,
                            metadata_json=metadata.model_dump(mode="json"),
                            content_hash=metadata.content_hash,
                            status=CandidateState.FOUND,
                        )
                    )
                    self.session.add(
                        ProcessingHistory(
                            entity_type="video_source",
                            entity_id=video.id,
                            action="discovery",
                            event="video_found",
                            result={"query_id": run_id, "platform": metadata.platform},
                        )
                    )
                    await self.session.flush()
                    candidate.video_id = video.id
                    found_count += 1
                    await self.event_bus.publish(
                        VideoFound(
                            query_id=run_id,
                            platform=metadata.platform,
                            video_id=video.id,
                            url=str(metadata.url),
                        )
                    )
                    candidates.append(candidate)
            except (ConnectorError, ValueError, RuntimeError) as error:
                errors.append(f"{connector.platform}: {error}")
        await self.event_bus.publish(
            DiscoveryCompleted(
                query_id=run_id,
                found_count=found_count,
                filtered_count=filtered_count,
            )
        )
        return DiscoveryResult(
            query_id=run_id,
            candidates=candidates,
            found_count=found_count,
            filtered_count=filtered_count,
            errors=errors,
        )
