"""Persistence-aware workflow execution engine."""

import asyncio
from collections.abc import Callable
from datetime import UTC, datetime
from time import monotonic
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from ...core.events import (
    EventBus,
    TaskCompleted,
    TaskFailed,
    TaskStarted,
    WorkflowCompleted,
    WorkflowFailed,
    WorkflowStarted,
)
from ...database.models import Workflow as WorkflowModel
from ...repositories.workflows import WorkflowRepository
from .executor import TaskExecutor
from .retry import RetryPolicy, execute_with_retry
from .schemas import (
    TaskResult,
    TaskState,
    WorkflowDefinition,
    WorkflowRunResult,
    WorkflowState,
    WorkflowTaskDefinition,
)
from .state import InvalidWorkflowTransition, TaskLifecycle, WorkflowLifecycle
from .tasks import TaskContext, TaskRegistry, default_task_registry


class WorkflowNotFoundError(LookupError):
    """Raised when a workflow id is not persisted."""


class WorkflowEngine:
    """Load, execute, persist, and publish one workflow instance."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        event_bus: EventBus,
        tasks: TaskRegistry | None = None,
    ) -> None:
        self.session = session
        self.event_bus = event_bus
        self.tasks = tasks or default_task_registry()
        self.executor = TaskExecutor()

    async def _load(self, workflow_id: str) -> WorkflowModel:
        workflow = await WorkflowRepository(self.session).get_with_tasks(workflow_id)
        if workflow is None:
            raise WorkflowNotFoundError(f"workflow not found: {workflow_id}")
        return workflow

    @staticmethod
    def _definition(workflow: WorkflowModel) -> WorkflowDefinition:
        return WorkflowDefinition.model_validate(workflow.definition_json)

    @staticmethod
    def _state(status: str) -> WorkflowState:
        return WorkflowState.CREATED if status == "pending" else WorkflowState(status)

    async def execute(
        self,
        workflow_id: str,
        *,
        mode: str = "sequential",
        cancellation: asyncio.Event | None = None,
        terminal_cancellation: Callable[[], bool] | None = None,
    ) -> WorkflowRunResult:
        """Execute a workflow DAG and return a persisted progress summary."""
        workflow = await self._load(workflow_id)
        lifecycle = WorkflowLifecycle(self._state(workflow.status))
        if lifecycle.state in {
            WorkflowState.COMPLETED,
            WorkflowState.CANCELLED,
        }:
            return self._summary(workflow, [])
        try:
            lifecycle.transition(WorkflowState.RUNNING)
        except InvalidWorkflowTransition as error:
            raise WorkflowNotFoundError(str(error)) from error
        workflow.status = WorkflowState.RUNNING
        workflow.started_at = workflow.started_at or datetime.now(UTC)
        await self.session.flush()
        await self.event_bus.publish(WorkflowStarted(workflow_id=workflow_id))

        definition = self._definition(workflow)
        model_by_name = {task.task_type: task for task in workflow.tasks}
        results: list[TaskResult] = []
        errors: list[str] = list(workflow.errors_json or [])
        completed = 0
        session_lock = asyncio.Lock()

        async def run_task(task_definition: WorkflowTaskDefinition) -> TaskResult:
            nonlocal completed
            task_model = model_by_name.get(task_definition.name)
            if task_model is None:
                raise RuntimeError(f"persisted task missing: {task_definition.name}")
            task_lifecycle = TaskLifecycle(TaskState(task_model.status))
            task_lifecycle.transition(TaskState.RUNNING)
            task_model.status = TaskState.RUNNING
            await self.session.flush()
            await self.event_bus.publish(
                TaskStarted(workflow_id=workflow_id, task_id=task_model.id)
            )
            started = monotonic()
            context = TaskContext(
                workflow_id=workflow_id,
                task_id=task_model.id,
                input=task_definition.input,
            )

            async def operation() -> Any:
                if cancellation and cancellation.is_set():
                    raise asyncio.CancelledError
                task_model.attempts += 1
                task_model.status = TaskState.RUNNING
                async with session_lock:
                    await self.session.flush()
                return await self.tasks.execute(task_definition.task_type, context)

            async def mark_retry(attempt: int, error: Exception) -> None:
                task_model.status = TaskState.RETRYING
                task_model.error = f"attempt {attempt}: {error}"
                async with session_lock:
                    await self.session.flush()

            try:
                output, attempts = await execute_with_retry(
                    operation,
                    RetryPolicy(
                        max_attempts=task_definition.max_attempts,
                        initial_delay_seconds=task_definition.retry_delay_seconds,
                    ),
                    cancellation=cancellation,
                    on_retry=mark_retry,
                )
                task_model.status = TaskState.SUCCESS
                task_model.result = output.output
                task_model.error = None
                async with session_lock:
                    await self.session.flush()
                completed += 1
                workflow.current_step = task_definition.name
                workflow.progress = completed / len(definition.tasks) * 100
                result = TaskResult(
                    task_id=task_model.id,
                    task_type=task_definition.task_type,
                    status=TaskState.SUCCESS,
                    output=output.output,
                    attempts=attempts,
                    duration_seconds=max(0, monotonic() - started),
                )
                results.append(result)
                await self.event_bus.publish(
                    TaskCompleted(workflow_id=workflow_id, task_id=task_model.id)
                )
                return result
            except asyncio.CancelledError:
                task_model.status = TaskState.CANCELLED
                async with session_lock:
                    await self.session.flush()
                raise
            except Exception as error:
                task_model.status = TaskState.FAILED
                task_model.error = str(error)
                errors.append(str(error))
                async with session_lock:
                    await self.session.flush()
                await self.event_bus.publish(
                    TaskFailed(
                        workflow_id=workflow_id,
                        task_id=task_model.id,
                        error=str(error),
                    )
                )
                raise

        try:
            await self.executor.execute(
                definition.tasks,
                run_task,
                mode=mode,
                cancellation=cancellation,
                max_concurrency=definition.max_concurrency,
            )
        except asyncio.CancelledError:
            workflow.status = (
                WorkflowState.CANCELLED
                if terminal_cancellation and terminal_cancellation()
                else WorkflowState.PAUSED
            )
            workflow.errors_json = errors
            await self.session.flush()
            return self._summary(workflow, results, errors)
        except Exception as error:
            message = str(error)
            if message not in errors:
                errors.append(message)
            workflow.status = WorkflowState.FAILED
            workflow.errors_json = errors
            workflow.completed_at = datetime.now(UTC)
            await self.session.flush()
            await self.event_bus.publish(
                WorkflowFailed(workflow_id=workflow_id, error=message)
            )
            return self._summary(workflow, results, errors)

        workflow.status = WorkflowState.COMPLETED
        workflow.progress = 100
        workflow.completed_at = datetime.now(UTC)
        workflow.errors_json = errors
        await self.session.flush()
        await self.event_bus.publish(WorkflowCompleted(workflow_id=workflow_id))
        return self._summary(workflow, results, errors)

    @staticmethod
    def _summary(
        workflow: WorkflowModel,
        results: list[TaskResult],
        errors: list[str] | None = None,
    ) -> WorkflowRunResult:
        """Build a stable execution summary from persisted state."""
        return WorkflowRunResult(
            workflow_id=workflow.id,
            state=WorkflowState(
                WorkflowState.CREATED
                if workflow.status == "pending"
                else workflow.status
            ),
            completed_tasks=len(results),
            total_tasks=len(workflow.tasks),
            progress=workflow.progress,
            results=results,
            errors=list(errors if errors is not None else workflow.errors_json or []),
        )
