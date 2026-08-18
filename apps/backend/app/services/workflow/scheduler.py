"""In-process workflow queue and cancellation adapter."""

import asyncio
from dataclasses import dataclass, field
from uuid import uuid4

from ...tasks.base import AsyncTaskRunner


@dataclass(frozen=True, slots=True)
class WorkflowJob:
    """Queued workflow operation descriptor."""

    workflow_id: str
    job_id: str = field(default_factory=lambda: str(uuid4()))


class WorkflowScheduler:
    """Queue facade enforcing shared task limits and cancellation signals."""

    def __init__(self, runner: AsyncTaskRunner) -> None:
        self.runner = runner
        self._cancellations: dict[str, asyncio.Event] = {}
        self._terminal_cancellations: set[str] = set()

    def cancellation_for(self, workflow_id: str) -> asyncio.Event:
        """Return the shared cancellation signal for a workflow."""
        return self._cancellations.setdefault(workflow_id, asyncio.Event())

    def submit(self, workflow_id: str, operation: object) -> WorkflowJob:
        """Submit an async operation to the shared runner."""
        if not callable(operation):
            raise TypeError("workflow operation must be callable")
        self.runner.submit(operation)  # type: ignore[arg-type]
        return WorkflowJob(workflow_id=workflow_id)

    def cancel(self, workflow_id: str, *, terminal: bool = False) -> None:
        """Signal cancellation without forcefully killing task code."""
        if terminal:
            self._terminal_cancellations.add(workflow_id)
        self.cancellation_for(workflow_id).set()

    def reset(self, workflow_id: str) -> None:
        """Clear a prior cancellation signal before resuming work."""
        self._cancellations[workflow_id] = asyncio.Event()
        self._terminal_cancellations.discard(workflow_id)

    def is_terminally_cancelled(self, workflow_id: str) -> bool:
        """Report whether cancellation should end rather than pause work."""
        return workflow_id in self._terminal_cancellations

    @property
    def active_count(self) -> int:
        """Expose shared active job count for monitoring."""
        return self.runner.active_count
