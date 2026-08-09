"""Typed in-process events emitted by the deployable application boundary."""

from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Event:
    """Base event carrying correlation metadata."""

    event_id: str = field(default_factory=lambda: str(uuid4()))
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None


@dataclass(frozen=True, slots=True)
class AgentEvent(Event):
    """Base event for an agent lifecycle transition."""

    agent_id: str = ""
    run_id: str | None = None


class AgentCreated(AgentEvent):
    """Published after an agent definition is persisted."""


class AgentActivated(AgentEvent):
    """Published after an agent becomes active."""


class AgentStarted(AgentEvent):
    """Published when an agent execution begins."""


class AgentCompleted(AgentEvent):
    """Published after an agent execution completes."""


@dataclass(frozen=True, slots=True)
class AgentFailed(AgentEvent):
    """Published after an agent execution fails."""

    error: str = ""


@dataclass(frozen=True, slots=True)
class WorkflowEvent(Event):
    """Base event for workflow and task execution."""

    workflow_id: str = ""
    task_id: str | None = None


class WorkflowCreated(WorkflowEvent):
    """Published after a workflow instance is persisted."""


class WorkflowStarted(WorkflowEvent):
    """Published when workflow execution begins."""


class TaskStarted(WorkflowEvent):
    """Published when one workflow task begins."""


class TaskCompleted(WorkflowEvent):
    """Published when one workflow task succeeds."""


@dataclass(frozen=True, slots=True)
class TaskFailed(WorkflowEvent):
    """Published when one workflow task exhausts its retry policy."""

    error: str = ""


class WorkflowCompleted(WorkflowEvent):
    """Published when every workflow task succeeds."""


@dataclass(frozen=True, slots=True)
class WorkflowFailed(WorkflowEvent):
    """Published when a workflow stops after task failure."""

    error: str = ""


@dataclass(frozen=True, slots=True)
class DiscoveryEvent(Event):
    """Base event for one discovery query."""

    query_id: str = ""
    platform: str | None = None


class DiscoveryStarted(DiscoveryEvent):
    """Published when source searching starts."""


@dataclass(frozen=True, slots=True)
class VideoFound(DiscoveryEvent):
    """Published when a new metadata candidate is stored."""

    video_id: str = ""
    url: str = ""


@dataclass(frozen=True, slots=True)
class VideoFiltered(DiscoveryEvent):
    """Published when a candidate is rejected by filtering or deduplication."""

    url: str = ""
    reason: str = ""


@dataclass(frozen=True, slots=True)
class DiscoveryCompleted(DiscoveryEvent):
    """Published when all configured source connectors finish."""

    found_count: int = 0
    filtered_count: int = 0


@dataclass(frozen=True, slots=True)
class DuplicateDetected(DiscoveryEvent):
    """Published when an exact or near duplicate is identified."""

    url: str = ""
    reason: str = ""


EventHandler = Callable[[Event], Awaitable[None]]


class EventBus:
    """Small replaceable event adapter for local orchestration."""

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], handler: EventHandler) -> None:
        """Register an asynchronous handler for one event type."""
        self._handlers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        """Deliver an event to handlers registered for its concrete type."""
        for handler in tuple(self._handlers[type(event)]):
            await handler(event)
