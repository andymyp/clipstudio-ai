"""Backend core security and async task foundation tests."""

import asyncio

import pytest

from apps.backend.app.core.security import (
    AllowListPermissionChecker,
    LocalTokenValidator,
)
from apps.backend.app.tasks.base import AsyncTaskRunner


def test_local_token_validator_and_permissions() -> None:
    validator = LocalTokenValidator("secret-value")
    permissions = AllowListPermissionChecker({"system:read": True})

    assert validator.validate("secret-value") is True
    assert validator.validate("wrong-value") is False
    assert permissions.allowed("system:read") is True
    assert permissions.allowed("admin:write") is False


@pytest.mark.asyncio
async def test_async_task_runner_tracks_and_releases_tasks() -> None:
    runner = AsyncTaskRunner()
    completed = asyncio.Event()

    async def operation() -> None:
        completed.set()

    runner.submit(operation)
    await asyncio.wait_for(completed.wait(), timeout=1)
    await asyncio.sleep(0)

    assert runner.active_count == 0
