"""System metrics and version endpoints."""

from time import monotonic

from fastapi import APIRouter

from ...core.config import get_settings
from ...schemas.common import ApiResponse, SystemInfo

router = APIRouter(tags=["system"])
_started_at = monotonic()


@router.get("/system/info", response_model=ApiResponse[SystemInfo])
async def system_info() -> ApiResponse[SystemInfo]:
    """Return safe runtime information."""
    settings = get_settings()
    return ApiResponse(
        success=True,
        data=SystemInfo(
            name=settings.app.name,
            version=settings.app.version,
            environment=settings.app.environment,
            debug=settings.app.debug,
        ),
    )


@router.get("/metrics", response_model=ApiResponse[dict[str, float]])
async def metrics() -> ApiResponse[dict[str, float]]:
    """Return lightweight process metrics without optional system dependencies."""
    return ApiResponse(success=True, data={"uptime_seconds": monotonic() - _started_at})


@router.get("/version", response_model=ApiResponse[dict[str, str]])
async def version() -> ApiResponse[dict[str, str]]:
    """Return the application version."""
    settings = get_settings()
    return ApiResponse(
        success=True, data={"name": settings.app.name, "version": settings.app.version}
    )


@router.get("/config", response_model=ApiResponse[dict[str, object]])
async def configuration() -> ApiResponse[dict[str, object]]:
    """Return diagnostics-safe configuration without secrets."""
    return ApiResponse(success=True, data=get_settings().public_dict())
