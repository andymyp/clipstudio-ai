"""Small asynchronous event bus for decoupled foundation components."""

from collections import defaultdict
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class Event:
    """Base event carrying correlation metadata."""

    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    correlation_id: str | None = None


class AgentStarted(Event):
    """Published when an agent begins work."""


class VideoDiscovered(Event):
    """Published when a source is discovered."""


class AnalysisCompleted(Event):
    """Published when analysis completes."""


class ClipRendered(Event):
    """Published when a clip render completes."""


EventHandler = Callable[[Event], Awaitable[None]]


class EventBus:
    """In-process async event bus; external brokers can replace this adapter later."""

    def __init__(self) -> None:
        self._handlers: dict[type[Event], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: type[Event], handler: EventHandler) -> None:
        self._handlers[event_type].append(handler)

    async def publish(self, event: Event) -> None:
        for handler in self._handlers[type(event)]:
            await handler(event)
