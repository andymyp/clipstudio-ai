"""Agent lifecycle, tool, memory, event, and persistence integration tests."""

import asyncio
from pathlib import Path

import pytest
import pytest_asyncio

from apps.backend.app.core.events import (
    AgentActivated,
    AgentCompleted,
    AgentCreated,
    AgentStarted,
    Event,
    EventBus,
)
from apps.backend.app.database.base import Base
from apps.backend.app.database.engine import Database
from apps.backend.app.schemas.entities import AgentCreate
from apps.backend.app.services.agents.agent import Agent
from apps.backend.app.services.agents.lifecycle import (
    AgentLifecycle,
    InvalidAgentTransition,
)
from apps.backend.app.services.agents.manager import AgentManager
from apps.backend.app.services.agents.memory import (
    InMemorySemanticMemory,
    LongTermMemory,
    ShortTermMemory,
)
from apps.backend.app.services.agents.schemas import (
    AgentConfiguration,
    AgentGoal,
    AgentObservation,
    AgentState,
)
from apps.backend.app.services.agents.tools import FunctionTool, ToolRegistry
from apps.backend.app.tasks.base import AsyncTaskRunner
from backend.app.core.config import DatabaseConfig, Settings


@pytest.mark.asyncio
async def test_agent_decision_loop_tools_memory_and_events() -> None:
    """An active generic agent runs its bounded loop and publishes lifecycle events."""
    events: list[Event] = []
    bus = EventBus()

    async def collect(event: Event) -> None:
        events.append(event)

    bus.subscribe(AgentStarted, collect)
    bus.subscribe(AgentCompleted, collect)

    async def inspect(payload: dict[str, object]) -> dict[str, object]:
        return {"received": payload}

    registry = ToolRegistry([FunctionTool("inspect", "Test tool", inspect)])
    configuration = AgentConfiguration(
        name="Test agent",
        category="test",
        goal=AgentGoal(objective="Inspect the supplied context"),
        tools=["inspect"],
    )
    agent = Agent(
        agent_id="agent-test",
        configuration=configuration,
        event_bus=bus,
        tools=registry,
    )
    agent.activate()
    result = await agent.run(AgentObservation(data={"value": 3}))

    assert result.evaluation.success is True
    assert result.results[0]["tool"] == "inspect"
    assert agent.state == AgentState.ACTIVE
    assert len(agent.long_term.by_kind("successful_result")) == 1
    assert [type(event) for event in events] == [AgentStarted, AgentCompleted]


def test_lifecycle_and_memory_limits() -> None:
    """Unsafe transitions are rejected and memory stays bounded."""
    lifecycle = AgentLifecycle()
    with pytest.raises(InvalidAgentTransition):
        lifecycle.transition(AgentState.RUNNING)

    short_term = ShortTermMemory()
    short_term.update(task="task", context={"source": "test"})
    assert short_term.snapshot()["current_task"] == "task"

    long_term = LongTermMemory(max_records=2)
    long_term.remember("approved_clip", {"id": "1"})
    long_term.remember("rejected_clip", {"id": "2"})
    long_term.remember("feedback", {"id": "3"})
    assert len(long_term.records) == 2
    assert [record.kind for record in long_term.records] == [
        "rejected_clip",
        "feedback",
    ]


@pytest.mark.asyncio
async def test_semantic_memory_is_replaceable_without_vector_database() -> None:
    """The semantic port is usable while remaining independent of vector storage."""
    memory = InMemorySemanticMemory()
    await memory.store({"text": "viral funny moment"})
    await memory.store({"text": "quiet interview"})

    matches = await memory.search("funny")
    assert matches == [{"text": "viral funny moment"}]


@pytest_asyncio.fixture
async def agent_database(tmp_path: Path):
    """Provide an isolated database for manager integration."""
    database_path = (tmp_path / "agents.sqlite").as_posix()
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
async def test_agent_manager_persists_configuration_and_emits_events(
    agent_database: Database,
) -> None:
    """The manager connects persistence, lifecycle actions, execution, and events."""
    events: list[Event] = []
    bus = EventBus()

    async def collect(event: Event) -> None:
        events.append(event)

    for event_type in (AgentCreated, AgentActivated, AgentStarted, AgentCompleted):
        bus.subscribe(event_type, collect)

    async with agent_database.transaction() as session:
        manager = AgentManager(
            session=session,
            session_factory=agent_database.sessions,
            event_bus=bus,
            task_runner=AsyncTaskRunner(),
        )
        created = await manager.create(
            AgentCreate(
                name="Managed agent",
                category="test",
                description="Run a generic goal.",
                configuration={"tools": ["discovery"]},
            )
        )
        await manager.activate(created.id)
        result = await manager.execute(
            created.id, AgentObservation(data={"input": "value"})
        )

        assert result.evaluation.success is True
        assert (await manager.monitor(created.id)).state == AgentState.ACTIVE
        assert await manager.delete(created.id) is True

    assert [type(event) for event in events] == [
        AgentCreated,
        AgentActivated,
        AgentStarted,
        AgentCompleted,
    ]


@pytest.mark.asyncio
async def test_task_runner_resource_limit_is_enforced() -> None:
    """Agent execution can be bounded by the shared async runner."""
    runner = AsyncTaskRunner(max_active=1)
    blocker = asyncio.Event()

    async def operation() -> None:
        await blocker.wait()

    runner.submit(operation)
    await asyncio.sleep(0)
    with pytest.raises(RuntimeError, match="resource limit"):
        runner.submit(operation)
    blocker.set()
