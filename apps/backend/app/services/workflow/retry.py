"""Bounded retry policy for workflow task failures."""

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetryPolicy:
    """Exponential backoff policy with hard attempt and delay limits."""

    max_attempts: int = 3
    initial_delay_seconds: float = 0
    backoff_multiplier: float = 2
    max_delay_seconds: float = 3600

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.initial_delay_seconds < 0 or self.max_delay_seconds < 0:
            raise ValueError("retry delays cannot be negative")
        if self.backoff_multiplier < 1:
            raise ValueError("backoff_multiplier must be at least one")

    def delay_for(self, attempt: int) -> float:
        """Return the delay before the next attempt."""
        return min(
            self.max_delay_seconds,
            self.initial_delay_seconds * self.backoff_multiplier ** max(0, attempt - 1),
        )


async def execute_with_retry[T](
    operation: Callable[[], Awaitable[T]],
    policy: RetryPolicy,
    *,
    cancellation: asyncio.Event | None = None,
    on_retry: Callable[[int, Exception], Awaitable[None]] | None = None,
) -> tuple[T, int]:
    """Execute an operation until success, cancellation, or exhausted attempts."""
    last_error: Exception | None = None
    for attempt in range(1, policy.max_attempts + 1):
        if cancellation and cancellation.is_set():
            raise asyncio.CancelledError
        try:
            return await operation(), attempt
        except asyncio.CancelledError:
            raise
        except Exception as error:
            last_error = error
            if attempt >= policy.max_attempts:
                raise
            if on_retry:
                await on_retry(attempt, error)
            delay = policy.delay_for(attempt)
            if delay:
                await asyncio.sleep(delay)
    raise RuntimeError("retry loop exited without a result") from last_error
