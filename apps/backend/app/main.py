"""Production application factory for the backend boundary."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.errors import register_exception_handlers
from .api.health import router as health_router
from .api.router import api_router
from .core.config import get_settings
from .core.logging import configure_logging, get_logger
from .dependencies.container import get_container
from .middleware.error import ErrorCaptureMiddleware
from .middleware.logging import RequestLoggingMiddleware


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Initialize and shut down process-level infrastructure."""
    settings = get_settings()
    container = get_container()
    configure_logging(settings)
    logger = get_logger("clipstudio.application")
    await container.database.start()
    logger.info("application_starting", extra={"event": "application_starting"})
    yield
    logger.info("application_stopping", extra={"event": "application_stopping"})
    container.task_runner.cancel_all()
    await container.database.dispose()


def create_app() -> FastAPI:
    """Compose the API, middleware, error policy, and lifecycle."""
    settings = get_settings()
    application = FastAPI(
        title=settings.app.name,
        version=settings.app.version,
        description="Local-first AI content production control plane.",
        lifespan=lifespan,
    )
    application.add_middleware(ErrorCaptureMiddleware)
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    application.include_router(health_router)
    application.include_router(api_router)
    register_exception_handlers(application)
    return application


app = create_app()

__all__ = ["app", "create_app"]
