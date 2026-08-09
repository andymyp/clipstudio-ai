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
