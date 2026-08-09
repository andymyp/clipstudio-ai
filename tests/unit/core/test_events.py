"""Event bus tests."""

import pytest

from backend.app.core.events import Event, EventBus


@pytest.mark.asyncio
async def test_event_bus_publishes_to_subscriber() -> None:
    received: list[Event] = []
    bus = EventBus()

    async def handler(event: Event) -> None:
        received.append(event)

    bus.subscribe(Event, handler)
    event = Event()
    await bus.publish(event)

    assert received == [event]
