"""Database session dependency boundary."""

from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.database.session import database_health as _database_health

from ..core.config import Settings
from .engine import Database


async def get_session(database: Database) -> AsyncIterator[AsyncSession]:
    """Yield a request-scoped session with transaction handling."""
    async with database.transaction() as session:
        yield session


def create_database(settings: Settings) -> Database:
    """Create an injectable database lifecycle object."""
    return Database(settings)


async def database_health(database_url: str) -> str:
    """Compatibility health probe used by the public health routes."""
    return await _database_health(database_url)


__all__ = ["Database", "create_database", "database_health", "get_session"]
