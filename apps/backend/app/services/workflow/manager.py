"""Workflow lifecycle manager and queue integration."""

from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ...core.events import EventBus, WorkflowCreated
from ...database.models import Workflow as WorkflowModel
from ...database.models import WorkflowTask
from ...repositories.workflows import WorkflowRepository
from .engine import WorkflowEngine, WorkflowNotFoundError
from .scheduler import WorkflowJob, WorkflowScheduler
from .schemas import WorkflowDefinition, WorkflowState
from .state import InvalidWorkflowTransition, WorkflowLifecycle
from .tasks import TaskRegistry, default_task_registry


class WorkflowOperationError(ValueError):
    """Raised when a workflow cannot perform a requested operation."""


TaskRegistryFactory = Callable[[], TaskRegistry]


class WorkflowManager:
    """Coordinate workflow definitions, state changes, execution, and queueing."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        session_factory: async_sessionmaker[AsyncSession],
        event_bus: EventBus,
        scheduler: WorkflowScheduler,
        tasks_factory: TaskRegistryFactory = default_task_registry,
    ) -> None:
        self.session = session
        self.session_factory = session_factory
        self.event_bus = event_bus
        self.scheduler = scheduler
        self.tasks_factory = tasks_factory

    async def _load(self, workflow_id: str) -> WorkflowModel:
        workflow = await WorkflowRepository(self.session).get_with_tasks(workflow_id)
        if workflow is None:
            raise WorkflowNotFoundError(f"workflow not found: {workflow_id}")
        return workflow

    def _engine(self, session: AsyncSession) -> WorkflowEngine:
        return WorkflowEngine(
            session=session,
            event_bus=self.event_bus,
            tasks=self.tasks_factory(),
        )

    async def create(self, definition: WorkflowDefinition) -> WorkflowModel:
        """Persist a workflow instance and its task graph."""
        workflow = await WorkflowRepository(self.session).create(
            WorkflowModel(
                agent_id=definition.agent_id,
                status=WorkflowState.CREATED,
                definition_json=definition.model_dump(mode="json"),
                errors_json=[],
            )
        )
        for task in definition.tasks:
            self.session.add(
                WorkflowTask(
                    workflow_id=workflow.id,
                    task_type=task.name,
                    status="pending",
                    input_json=dict(task.input),
                    depends_on=list(task.dependencies),
                    max_attempts=task.max_attempts,
                )
            )
        await self.session.flush()
        await self.event_bus.publish(WorkflowCreated(workflow_id=workflow.id))
        return workflow

    async def queue(self, workflow_id: str) -> WorkflowModel:
        """Move a workflow to the queue without executing it yet."""
        workflow = await self._load(workflow_id)
        lifecycle = WorkflowLifecycle(
            WorkflowState.CREATED
            if workflow.status == "pending"
            else WorkflowState(workflow.status)
        )
        try:
            lifecycle.transition(WorkflowState.QUEUED)
        except InvalidWorkflowTransition as error:
            raise WorkflowOperationError(str(error)) from error
        workflow.status = lifecycle.state
        await WorkflowRepository(self.session).update(workflow)
        return workflow

    async def execute(self, workflow_id: str, *, mode: str = "sequential"):
        """Execute one workflow in the caller's transaction."""
        return await self._engine(self.session).execute(
            workflow_id,
            mode=mode,
            cancellation=self.scheduler.cancellation_for(workflow_id),
            terminal_cancellation=lambda: self.scheduler.is_terminally_cancelled(
                workflow_id
            ),
        )

    async def enqueue(
        self, workflow_id: str, *, mode: str = "sequential"
    ) -> WorkflowJob:
        """Queue a workflow in a fresh worker session."""
        await self.queue(workflow_id)

        async def operation() -> None:
            async with self.session_factory() as worker_session:
                await self._engine(worker_session).execute(
                    workflow_id,
                    mode=mode,
                    cancellation=self.scheduler.cancellation_for(workflow_id),
                    terminal_cancellation=lambda: self.scheduler.is_terminally_cancelled(
                        workflow_id
                    ),
                )
                await worker_session.commit()

        try:
            return self.scheduler.submit(workflow_id, operation)
        except (RuntimeError, TypeError) as error:
            raise WorkflowOperationError(str(error)) from error

    async def pause(self, workflow_id: str) -> WorkflowModel:
        """Pause queued/running execution through a shared cancellation signal."""
        workflow = await self._load(workflow_id)
        state = (
            WorkflowState.CREATED
            if workflow.status == "pending"
            else WorkflowState(workflow.status)
        )
        lifecycle = WorkflowLifecycle(state)
        try:
            lifecycle.transition(WorkflowState.PAUSED)
        except InvalidWorkflowTransition as error:
            raise WorkflowOperationError(str(error)) from error
        self.scheduler.cancel(workflow_id)
        workflow.status = WorkflowState.PAUSED
        await WorkflowRepository(self.session).update(workflow)
        return workflow

    async def resume(self, workflow_id: str) -> WorkflowJob:
        """Clear cancellation and queue a paused workflow again."""
        self.scheduler.reset(workflow_id)
        workflow = await self._load(workflow_id)
        if workflow.status != WorkflowState.PAUSED:
            raise WorkflowOperationError("only paused workflows can be resumed")
        workflow.status = WorkflowState.QUEUED
        await WorkflowRepository(self.session).update(workflow)
        return await self.enqueue(workflow_id)

    async def cancel(self, workflow_id: str) -> WorkflowModel:
        """Cancel queued or running work and signal its worker."""
        workflow = await self._load(workflow_id)
        if workflow.status not in {
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }:
            self.scheduler.cancel(workflow_id, terminal=True)
            workflow.status = WorkflowState.CANCELLED
            workflow.completed_at = datetime.now(UTC)
            await WorkflowRepository(self.session).update(workflow)
        return workflow

    async def delete(self, workflow_id: str) -> bool:
        """Delete a workflow and its persisted task rows."""
        deleted = await WorkflowRepository(self.session).delete(workflow_id)
        if not deleted:
            raise WorkflowNotFoundError(f"workflow not found: {workflow_id}")
        return True

    async def monitor(self, workflow_id: str) -> WorkflowModel:
        """Load current state for monitoring adapters."""
        return await self._load(workflow_id)
