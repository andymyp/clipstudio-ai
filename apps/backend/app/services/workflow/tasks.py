"""Independent workflow task contracts and plugin registry."""

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field


class TaskInput(BaseModel):
    """Generic task input schema for replaceable domain tasks."""

    model_config = ConfigDict(extra="allow")

    data: dict[str, Any] = Field(default_factory=dict)


class TaskOutput(BaseModel):
    """Generic task output schema."""

    output: dict[str, Any] = Field(default_factory=dict)


class TaskContext(BaseModel):
    """Execution context supplied to a task implementation."""

    workflow_id: str
    task_id: str
    input: dict[str, Any] = Field(default_factory=dict)


class WorkflowTask(Protocol):
    """Task plugin interface with execution and rollback ports."""

    name: str
    description: str
    input_schema: type[BaseModel]
    output_schema: type[TaskOutput]

    async def execute(self, context: TaskContext) -> TaskOutput:
        """Execute one independent task."""

    async def rollback(self, context: TaskContext, result: TaskOutput) -> None:
        """Undo task side effects when a later workflow step fails."""


TaskHandler = Callable[[TaskContext], Awaitable[dict[str, Any]]]


class FunctionTask:
    """Adapter for an independently implemented async task function."""

    input_schema: type[BaseModel] = TaskInput
    output_schema: type[TaskOutput] = TaskOutput

    def __init__(self, name: str, description: str, handler: TaskHandler) -> None:
        self.name = name
        self.description = description
        self._handler = handler

    async def execute(self, context: TaskContext) -> TaskOutput:
        """Validate input, call the handler, and normalize output."""
        validated = self.input_schema.model_validate(context.input)
        output = await self._handler(
            context.model_copy(update={"input": validated.model_dump()})
        )
        return self.output_schema(output=output)

    async def rollback(self, context: TaskContext, result: TaskOutput) -> None:
        """Default no-op rollback for side-effect-free task adapters."""


class DeferredTask(FunctionTask):
    """Safe orchestration port for a future domain service."""

    def __init__(self, name: str, description: str) -> None:
        async def deferred(context: TaskContext) -> dict[str, Any]:
            return {"accepted": True, "task": name, "input": context.input}

        super().__init__(name, description, deferred)


class TaskRegistry:
    """Name-based plugin registry keeping tasks independent from the engine."""

    def __init__(self, tasks: list[WorkflowTask] | None = None) -> None:
        self._tasks: dict[str, WorkflowTask] = {}
        for task in tasks or []:
            self.register(task)

    def register(self, task: WorkflowTask) -> None:
        """Register one unique task implementation."""
        if task.name in self._tasks:
            raise ValueError(f"task already registered: {task.name}")
        self._tasks[task.name] = task

    def get(self, name: str) -> WorkflowTask:
        """Resolve a task or raise a configuration error."""
        try:
            return self._tasks[name]
        except KeyError as error:
            raise KeyError(f"task not registered: {name}") from error

    async def execute(self, name: str, context: TaskContext) -> TaskOutput:
        """Execute a named task plugin."""
        return await self.get(name).execute(context)


def default_task_registry() -> TaskRegistry:
    """Build the default clip-pipeline ports without domain implementations."""
    names = (
        "discovery",
        "transcript",
        "analysis",
        "scoring",
        "segment_download",
        "subtitle",
        "rendering",
        "quality_check",
        "storage",
    )
    return TaskRegistry(
        [DeferredTask(name, f"Deferred {name} pipeline task.") for name in names]
    )


__all__ = ["FunctionTask", "TaskContext", "TaskOutput", "TaskRegistry", "WorkflowTask"]
