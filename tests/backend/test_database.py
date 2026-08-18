"""Database model, transaction, and repository integration tests."""

from pathlib import Path

import pytest
import pytest_asyncio
from pydantic import ValidationError
from sqlalchemy import select

from apps.backend.app.database.base import Base
from apps.backend.app.database.engine import Database
from apps.backend.app.database.models import (
    Agent,
    Clip,
    Transcript,
    VideoSource,
    Workflow,
    WorkflowTask,
)
from apps.backend.app.database.seed import seed_defaults
from apps.backend.app.repositories.agents import AgentRepository
from apps.backend.app.repositories.clips import ClipRepository
from apps.backend.app.repositories.models import ModelRepository
from apps.backend.app.repositories.videos import VideoRepository
from apps.backend.app.repositories.workflows import WorkflowRepository
from apps.backend.app.schemas.entities import AgentCreate, VideoSourceCreate
from backend.app.core.config import DatabaseConfig, Settings


@pytest_asyncio.fixture
async def database(tmp_path: Path):
    """Provide an isolated SQLite database with the model metadata installed."""
    database_path = (tmp_path / "database.sqlite").as_posix()
    settings = Settings(
        database=DatabaseConfig(url=f"sqlite+aiosqlite:///{database_path}")
    )
    database = Database(settings)
    await database.start()
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield database
    await database.dispose()


@pytest.mark.asyncio
async def test_models_relationships_and_repositories(database: Database) -> None:
    async with database.transaction() as session:
        agent = Agent(name="Test Agent", category="test")
        video = VideoSource(
            agent=agent,
            url="https://example.com/video-1",
            platform="example",
            title="Example Video",
        )
        transcript = Transcript(video_source=video, text="hello", language="en")
        workflow = Workflow(agent=agent, status="pending")
        task = WorkflowTask(workflow=workflow, task_type="test", status="pending")
        clip = Clip(source_video=video, agent=agent, status="review")
        session.add_all([agent, video, transcript, workflow, task, clip])
        await session.flush()
        agent_id = agent.id
        video_id = video.id
        clip_id = clip.id

    async with database.transaction() as session:
        assert (await AgentRepository(session).get(agent_id)) is not None
        assert (
            await VideoRepository(session).get_by_url("https://example.com/video-1")
        ) is not None
        assert len(await WorkflowRepository(session).list_pending()) == 1
        assert len(await ClipRepository(session).list_by_status("review")) == 1
        loaded_video = await session.get(VideoSource, video_id)
        assert loaded_video is not None
        assert loaded_video.title == "Example Video"

        clip_repository = ClipRepository(session)
        loaded_clip = await clip_repository.get(clip_id)
        assert loaded_clip is not None
        loaded_clip.status = "approved"
        await clip_repository.update(loaded_clip)

    async with database.transaction() as session:
        assert len(await ClipRepository(session).list_by_status("approved")) == 1
        assert len((await session.execute(select(Transcript))).scalars().all()) == 1


@pytest.mark.asyncio
async def test_seed_is_idempotent(database: Database) -> None:
    async with database.transaction() as session:
        await seed_defaults(session)
    async with database.transaction() as session:
        await seed_defaults(session)
        models = await ModelRepository(session).list_available()

    assert [model.name for model in models] == ["disabled"]


def test_entity_input_validation() -> None:
    agent = AgentCreate(name="Agent", category="analysis")
    source = VideoSourceCreate(url="https://example.com/video", platform="example")

    assert agent.name == "Agent"
    assert str(source.url) == "https://example.com/video"
    with pytest.raises(ValidationError):
        VideoSourceCreate(url="not-a-url", platform="example")
