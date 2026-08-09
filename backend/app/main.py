"""FastAPI application factory and process entry point."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging, get_logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize process-wide infrastructure and release it on shutdown."""
    settings = get_settings()
    configure_logging(settings)
    logger = get_logger(__name__)
    logger.info("application_starting", extra={"event": "application_starting"})
    yield
    logger.info("application_stopping", extra={"event": "application_stopping"})


def create_app() -> FastAPI:
    """Create a configured FastAPI instance."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description="Local-first AI content production control plane.",
        lifespan=lifespan,
    )
    application.include_router(router)
    return application


app = create_app()


__all__ = ["app", "create_app"]
