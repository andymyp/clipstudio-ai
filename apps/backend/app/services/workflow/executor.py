"""Dependency-aware sequential and parallel task executor."""

import asyncio
from collections.abc import Awaitable, Callable

from .schemas import WorkflowTaskDefinition


class WorkflowExecutionError(RuntimeError):
    """Raised for invalid task graphs or failed task execution."""


TaskRunner = Callable[[WorkflowTaskDefinition], Awaitable[object]]


class TaskExecutor:
    """Execute independent ready tasks concurrently and dependent tasks in order."""

    async def execute(
        self,
        definitions: list[WorkflowTaskDefinition],
        runner: TaskRunner,
        *,
        mode: str = "sequential",
        cancellation: asyncio.Event | None = None,
        max_concurrency: int = 2,
    ) -> list[object]:
        """Run a validated DAG in sequential or bounded parallel mode."""
        if mode not in {"sequential", "parallel"}:
            raise ValueError("mode must be sequential or parallel")
        if max_concurrency < 1:
            raise ValueError("max_concurrency must be positive")
        by_name = {definition.name: definition for definition in definitions}
        if len(by_name) != len(definitions):
            raise WorkflowExecutionError("workflow task names must be unique")
        for definition in definitions:
            missing = set(definition.dependencies) - by_name.keys()
            if missing:
                raise WorkflowExecutionError(
                    f"task {definition.name} has missing dependencies: {sorted(missing)}"
                )

        completed: set[str] = set()
        remaining = set(by_name)
        outputs: list[object] = []
        while remaining:
            if cancellation and cancellation.is_set():
                raise asyncio.CancelledError
            ready = [
                by_name[name]
                for name in remaining
                if set(by_name[name].dependencies).issubset(completed)
            ]
            ready.sort(key=lambda item: definitions.index(item))
            if not ready:
                raise WorkflowExecutionError(
                    "workflow task dependencies contain a cycle"
                )
            if mode == "sequential":
                for definition in ready:
                    outputs.append(await runner(definition))
                    completed.add(definition.name)
                    remaining.remove(definition.name)
            else:
                for start in range(0, len(ready), max_concurrency):
                    batch = ready[start : start + max_concurrency]
                    batch_outputs = await asyncio.gather(
                        *(runner(definition) for definition in batch)
                    )
                    outputs.extend(batch_outputs)
                    completed.update(definition.name for definition in batch)
                    remaining.difference_update(definition.name for definition in batch)
        return outputs
