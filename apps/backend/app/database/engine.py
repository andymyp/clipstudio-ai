"""Async database engine lifecycle and SQLite tuning."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from ..core.config import Settings


class Database:
    """Own an async engine and session factory for one application process."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        kwargs: dict[str, Any] = {"echo": settings.database.echo, "pool_pre_ping": True}
        if settings.database.url.startswith("sqlite"):
            kwargs["connect_args"] = {"check_same_thread": False}
        else:
            kwargs["pool_size"] = settings.database.pool_size
        self.engine: AsyncEngine = create_async_engine(settings.database.url, **kwargs)
        self.sessions = async_sessionmaker(self.engine, expire_on_commit=False)

    async def start(self) -> None:
        """Verify connectivity and apply local SQLite safety pragmas."""
        async with self.engine.begin() as connection:
            if self.settings.database.url.startswith("sqlite"):
                await connection.execute(text("PRAGMA foreign_keys=ON"))
                await connection.execute(text("PRAGMA journal_mode=WAL"))
            else:
                await connection.execute(text("SELECT 1"))

    async def dispose(self) -> None:
        """Release pooled connections."""
        await self.engine.dispose()

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[AsyncSession]:
        """Yield a transactional session with rollback-on-error semantics."""
        async with self.sessions() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
