"""Workflow state, dependency, retry, event, and persistence tests."""

from pathlib import Path

import pytest
import pytest_asyncio

from apps.backend.app.core.events import (
    Event,
    EventBus,
    TaskCompleted,
    TaskFailed,
    TaskStarted,
    WorkflowCompleted,
    WorkflowCreated,
    WorkflowFailed,
    WorkflowStarted,
)
from apps.backend.app.database.base import Base
from apps.backend.app.database.engine import Database
from apps.backend.app.repositories.workflows import WorkflowRepository
from apps.backend.app.services.workflow.executor import (
    TaskExecutor,
    WorkflowExecutionError,
)
from apps.backend.app.services.workflow.manager import WorkflowManager
from apps.backend.app.services.workflow.scheduler import WorkflowScheduler
from apps.backend.app.services.workflow.schemas import (
    TaskState,
    WorkflowDefinition,
    WorkflowState,
    WorkflowTaskDefinition,
)
from apps.backend.app.services.workflow.state import (
    InvalidWorkflowTransition,
    TaskLifecycle,
    WorkflowLifecycle,
)
from apps.backend.app.services.workflow.tasks import FunctionTask, TaskRegistry
from apps.backend.app.tasks.base import AsyncTaskRunner
from backend.app.core.config import DatabaseConfig, Settings


@pytest_asyncio.fixture
async def workflow_database(tmp_path: Path):
    """Provide an isolated SQLite database with workflow tables."""
    database_path = (tmp_path / "workflows.sqlite").as_posix()
    settings = Settings(
        database=DatabaseConfig(url=f"sqlite+aiosqlite:///{database_path}")
    )
    database = Database(settings)
    await database.start()
    async with database.engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield database
    await database.dispose()


def test_workflow_and_task_state_machines_reject_invalid_transitions() -> None:
    """Workflow state is explicit and terminal states cannot restart."""
    workflow = WorkflowLifecycle()
    workflow.transition(WorkflowState.QUEUED)
    workflow.transition(WorkflowState.RUNNING)
    workflow.transition(WorkflowState.COMPLETED)
    with pytest.raises(InvalidWorkflowTransition):
        workflow.transition(WorkflowState.RUNNING)

    task = TaskLifecycle()
    task.transition(TaskState.RUNNING)
    task.transition(TaskState.RETRYING)
    task.transition(TaskState.RUNNING)
    task.transition(TaskState.SUCCESS)
    with pytest.raises(InvalidWorkflowTransition):
        task.transition(TaskState.FAILED)


@pytest.mark.asyncio
async def test_task_executor_respects_dependencies_and_parallel_mode() -> None:
    """The executor orders dependent tasks and can run independent tasks together."""
    definitions = [
        WorkflowTaskDefinition(name="first", task_type="first"),
        WorkflowTaskDefinition(
            name="second", task_type="second", dependencies=["first"]
        ),
        WorkflowTaskDefinition(name="independent", task_type="independent"),
    ]
    executed: list[str] = []

    async def run(definition: WorkflowTaskDefinition) -> str:
        executed.append(definition.name)
        return definition.name

    results = await TaskExecutor().execute(definitions, run, mode="parallel")

    assert results == ["first", "independent", "second"]
    assert executed.index("first") < executed.index("second")

    circular = [
        WorkflowTaskDefinition(name="a", task_type="a", dependencies=["b"]),
        WorkflowTaskDefinition(name="b", task_type="b", dependencies=["a"]),
    ]
    with pytest.raises(WorkflowExecutionError, match="cycle"):
        await TaskExecutor().execute(circular, run)


@pytest.mark.asyncio
async def test_workflow_engine_retries_tasks_persists_progress_and_publishes_events(
    workflow_database: Database,
) -> None:
    """A retryable workflow reaches completion with durable attempts and progress."""
    events: list[Event] = []
    bus = EventBus()

    async def collect(event: Event) -> None:
        events.append(event)

    for event_type in (
        WorkflowCreated,
        WorkflowStarted,
        TaskStarted,
        TaskCompleted,
        WorkflowCompleted,
    ):
        bus.subscribe(event_type, collect)

    attempts = 0

    async def flaky(_context: object) -> dict[str, bool]:
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise RuntimeError("temporary service failure")
        return {"ready": True}

    async def dependent(_context: object) -> dict[str, bool]:
        return {"dependent": True}

    registry = TaskRegistry(
        [
            FunctionTask("flaky", "Flaky test task", flaky),
            FunctionTask("dependent", "Dependent test task", dependent),
        ]
    )

    async with workflow_database.transaction() as session:
        manager = WorkflowManager(
            session=session,
            session_factory=workflow_database.sessions,
            event_bus=bus,
            scheduler=WorkflowScheduler(AsyncTaskRunner()),
            tasks_factory=lambda: registry,
        )
        workflow = await manager.create(
            WorkflowDefinition(
                name="Retry workflow",
                tasks=[
                    WorkflowTaskDefinition(
                        name="first", task_type="flaky", max_attempts=3
                    ),
                    WorkflowTaskDefinition(
                        name="second",
                        task_type="dependent",
                        dependencies=["first"],
                    ),
                ],
            )
        )
        result = await manager.execute(workflow.id)
        loaded = await WorkflowRepository(session).get_with_tasks(workflow.id)

        assert result.state == WorkflowState.COMPLETED
        assert result.progress == 100
        assert loaded is not None
        assert loaded.tasks[0].attempts == 3
        assert loaded.tasks[0].status == "success"
        assert [type(event) for event in events] == [
            WorkflowCreated,
            WorkflowStarted,
            TaskStarted,
            TaskCompleted,
            TaskStarted,
            TaskCompleted,
            WorkflowCompleted,
        ]


@pytest.mark.asyncio
async def test_workflow_failure_is_recovered_as_durable_failed_state(
    workflow_database: Database,
) -> None:
    """Exhausted retries persist task errors and publish failure events."""
    events: list[Event] = []
    bus = EventBus()

    async def collect(event: Event) -> None:
        events.append(event)

    bus.subscribe(TaskFailed, collect)
    bus.subscribe(WorkflowFailed, collect)

    async def failing(_context: object) -> dict[str, bool]:
        raise RuntimeError("permanent failure")

    registry = TaskRegistry([FunctionTask("failing", "Failing task", failing)])
    async with workflow_database.transaction() as session:
        manager = WorkflowManager(
            session=session,
            session_factory=workflow_database.sessions,
            event_bus=bus,
            scheduler=WorkflowScheduler(AsyncTaskRunner()),
            tasks_factory=lambda: registry,
        )
        workflow = await manager.create(
            WorkflowDefinition(
                name="Failure workflow",
                tasks=[
                    WorkflowTaskDefinition(
                        name="fail", task_type="failing", max_attempts=2
                    )
                ],
            )
        )
        result = await manager.execute(workflow.id)
        loaded = await WorkflowRepository(session).get_with_tasks(workflow.id)

        assert result.state == WorkflowState.FAILED
        assert result.errors == ["permanent failure"]
        assert loaded is not None
        assert loaded.tasks[0].attempts == 2
        assert loaded.tasks[0].status == "failed"
        assert [type(event) for event in events] == [TaskFailed, WorkflowFailed]
