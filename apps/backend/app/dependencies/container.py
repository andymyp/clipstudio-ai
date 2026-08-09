"""Dependency injection container for the application boundary."""

from dataclasses import dataclass
from functools import lru_cache
from logging import Logger

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..core.config import Settings, get_settings
from ..core.events import EventBus
from ..core.logging import get_logger
from ..database.session import Database, create_database
from ..tasks.base import AsyncTaskRunner


@dataclass(slots=True)
class AppContainer:
    """Composition root dependencies shared by request handlers."""

    settings: Settings
    logger: Logger
    database: Database
    event_bus: EventBus
    task_runner: AsyncTaskRunner

    @property
    def database_sessions(self) -> async_sessionmaker[AsyncSession]:
        """Create an injectable async session factory."""
        return self.database.sessions


@lru_cache(maxsize=1)
def get_container() -> AppContainer:
    """Return the process-level dependency container."""
    settings = get_settings()
    return AppContainer(
        settings=settings,
        logger=get_logger("clipstudio.container"),
        database=create_database(settings),
        event_bus=EventBus(),
        task_runner=AsyncTaskRunner(),
    )
