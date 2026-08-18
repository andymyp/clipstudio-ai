"""Discovery connector, normalization, filtering, deduplication, and storage tests."""

from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy import select

from apps.backend.app.core.events import (
    DiscoveryCompleted,
    DiscoveryStarted,
    DuplicateDetected,
    Event,
    EventBus,
    VideoFiltered,
    VideoFound,
)
from apps.backend.app.database.base import Base
from apps.backend.app.database.engine import Database
from apps.backend.app.database.models import Agent, ProcessingHistory
from apps.backend.app.repositories.videos import VideoRepository
from apps.backend.app.services.discovery.candidates import NoopSemanticDeduplicator
from apps.backend.app.services.discovery.connectors import (
    ConnectorRegistry,
    DeferredConnector,
    StaticConnector,
    default_connector_registry,
)
from apps.backend.app.services.discovery.manager import DiscoveryManager
from apps.backend.app.services.discovery.schemas import (
    CandidateState,
    DiscoveryFilters,
    DuplicateMatch,
    SearchQuery,
    VideoMetadata,
)
from apps.backend.app.services.discovery.templates import funny_moments_query
from backend.app.core.config import DatabaseConfig, Settings


@pytest_asyncio.fixture
async def discovery_database(tmp_path: Path):
    """Provide an isolated SQLite database for metadata discovery."""
    database_path = (tmp_path / "discovery.sqlite").as_posix()
    settings = Settings(
        database=DatabaseConfig(url=f"sqlite+aiosqlite:///{database_path}")
    )
    database = Database(settings)
    await database.start()
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield database
    await database.dispose()


def _metadata(url: str, *, title: str, duration: float = 30) -> VideoMetadata:
    """Build deterministic connector metadata for tests."""
    return VideoMetadata(
        title=title,
        description="  A   test description  ",
        author="Test Author",
        platform="test",
        url=url,
        duration=duration,
        view_count=1000,
        tags=["Funny", "funny", " test "],
    )


def test_connector_registry_and_query_templates_are_platform_agnostic() -> None:
    """Connectors load by platform and the example query remains declarative."""
    registry = default_connector_registry()
    assert set(registry.platforms()) == {"youtube", "tiktok", "instagram", "reddit"}
    assert isinstance(registry.get("youtube"), DeferredConnector)
    query, filters = funny_moments_query()
    assert query.text() == "funny interview moments funny viral moments"
    assert filters.max_duration == 180


@pytest.mark.asyncio
async def test_discovery_normalizes_filters_deduplicates_and_stores_history(
    discovery_database: Database,
) -> None:
    """Discovery stores accepted metadata and rejects filtered/duplicate candidates."""
    events: list[Event] = []
    bus = EventBus()

    async def collect(event: Event) -> None:
        events.append(event)

    for event_type in (
        DiscoveryStarted,
        VideoFound,
        VideoFiltered,
        DuplicateDetected,
        DiscoveryCompleted,
    ):
        bus.subscribe(event_type, collect)

    first = _metadata("https://example.com/one", title="  Funny   Moment  ")
    too_long = _metadata("https://example.com/two", title="Long Moment", duration=120)
    duplicate = _metadata("https://example.com/one", title="Same URL")
    connectors = ConnectorRegistry(
        [StaticConnector("test", [first, too_long, duplicate])]
    )

    async with discovery_database.transaction() as session:
        agent = Agent(name="Discovery Agent", category="test")
        session.add(agent)
        await session.flush()
        manager = DiscoveryManager(
            session=session,
            event_bus=bus,
            connectors=connectors,
        )
        result = await manager.discover(
            SearchQuery(keywords=["funny"], platforms=["test"], limit=10),
            filters=DiscoveryFilters(max_duration=60),
            agent_id=agent.id,
        )
        stored = await VideoRepository(session).get_by_url("https://example.com/one")
        history = (await session.execute(select(ProcessingHistory))).scalars().all()

        assert result.found_count == 1
        assert result.filtered_count == 2
        assert [candidate.state for candidate in result.candidates] == [
            CandidateState.FOUND,
            CandidateState.FILTERED,
            CandidateState.REJECTED,
        ]
        assert result.candidates[0].metadata.title == "Funny Moment"
        assert result.candidates[0].metadata.tags == ["funny", "test"]
        assert stored is not None
        assert stored.agent_id == agent.id
        assert len(history) == 1
        assert [type(event) for event in events] == [
            DiscoveryStarted,
            VideoFound,
            VideoFiltered,
            DuplicateDetected,
            VideoFiltered,
            DiscoveryCompleted,
        ]


@pytest.mark.asyncio
async def test_semantic_duplicate_port_can_reject_without_vector_database(
    discovery_database: Database,
) -> None:
    """A semantic deduplicator plugin participates after cheap URL checks."""

    class SemanticDuplicate(NoopSemanticDeduplicator):
        async def check(self, metadata: VideoMetadata) -> DuplicateMatch:
            return DuplicateMatch(
                duplicate=True, reason="semantic_duplicate", similarity=95
            )

    async with discovery_database.transaction() as session:
        manager = DiscoveryManager(
            session=session,
            event_bus=EventBus(),
            connectors=ConnectorRegistry(
                [
                    StaticConnector(
                        "test",
                        [_metadata("https://example.com/semantic", title="Similar")],
                    )
                ]
            ),
            semantic_deduplicator=SemanticDuplicate(),
        )
        result = await manager.discover(SearchQuery(platforms=["test"]))

        assert result.found_count == 0
        assert result.candidates[0].duplicate is True
        assert result.candidates[0].reason == "semantic_duplicate"


@pytest.mark.asyncio
async def test_discovery_workflow_task_returns_candidate_output(
    discovery_database: Database,
) -> None:
    """Discovery exposes a workflow task adapter without downloading media."""
    from apps.backend.app.services.discovery.manager import DiscoveryWorkflowTask
    from apps.backend.app.services.workflow.tasks import TaskContext

    async with discovery_database.transaction() as session:
        manager = DiscoveryManager(
            session=session,
            event_bus=EventBus(),
            connectors=ConnectorRegistry([StaticConnector("test", [])]),
        )
        task = DiscoveryWorkflowTask(manager.engine)
        output = await task.execute(
            TaskContext(
                workflow_id="workflow-test",
                task_id="task-test",
                input={"keywords": ["test"], "platforms": ["test"]},
            )
        )

        assert output.output["found_count"] == 0
