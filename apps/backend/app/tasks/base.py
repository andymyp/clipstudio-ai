"""Replaceable task and worker ports."""

import asyncio
from collections.abc import Callable, Coroutine
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Job:
    """A lightweight job descriptor without workflow semantics."""

    name: str
    id: UUID = field(default_factory=uuid4)


class Worker(Protocol):
    """Port implemented by future background workers."""

    async def run(self, job: Job) -> None:
        """Execute a job."""


class AsyncTaskRunner:
    """Small in-process runner for foundation-level async jobs."""

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task[None]] = set()

    def submit(
        self, operation: Callable[[], Coroutine[Any, Any, None]]
    ) -> asyncio.Task[None]:
        """Schedule an operation and retain its task handle."""
        task: asyncio.Task[None] = asyncio.create_task(operation())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    @property
    def active_count(self) -> int:
        """Return the number of currently scheduled operations."""
        return len(self._tasks)
