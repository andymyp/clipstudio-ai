"""Async SQLAlchemy session and connection health adapter."""

from collections.abc import AsyncIterator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def create_engine(database_url: str, *, echo: bool = False) -> AsyncEngine:
    """Create an async engine for the configured local database."""
    return create_async_engine(database_url, echo=echo, pool_pre_ping=True)


async def database_health(database_url: str) -> str:
    """Check the database connection without creating application tables."""
    engine = create_engine(database_url)
    try:
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
        return "ok"
    except Exception:
        return "unavailable"
    finally:
        await engine.dispose()


def session_factory(
    database_url: str, *, echo: bool = False
) -> async_sessionmaker[AsyncSession]:
    """Build an injectable async session factory."""
    engine = create_engine(database_url, echo=echo)
    return async_sessionmaker(engine, expire_on_commit=False)


async def session_scope(
    factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    """Yield a session and commit or roll back the unit of work."""
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
