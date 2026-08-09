"""Foundation API routes."""

from fastapi import APIRouter

from app.core.config import get_settings
from app.database.session import database_health

router = APIRouter()


@router.get("/health", tags=["system"])
async def health() -> dict[str, object]:
    """Return the health of the application and its local dependencies."""
    settings = get_settings()
    db_status = await database_health(settings.database.url)
    overall = "ok" if db_status == "ok" else "degraded"
    return {
        "status": overall,
        "application": "ok",
        "database": db_status,
        "service": "ok",
    }


@router.get("/api/v1/system/info", tags=["system"])
async def system_info() -> dict[str, object]:
    """Return non-sensitive runtime information."""
    settings = get_settings()
    return {
        "name": settings.app.name,
        "version": settings.app.version,
        "environment": settings.app.environment,
        "debug": settings.app.debug,
    }


@router.get("/api/v1/config", tags=["system"])
async def configuration() -> dict[str, object]:
    """Return safe, non-secret configuration for diagnostics."""
    return get_settings().public_dict()
