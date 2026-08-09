"""Non-sensitive system and configuration endpoints."""

from fastapi import APIRouter

from ..core.config import get_settings
from ..schemas.common import ApiResponse, SystemInfo

router = APIRouter(tags=["system"])


@router.get(
    "/system/info", response_model=ApiResponse[SystemInfo], summary="System information"
)
async def system_info() -> ApiResponse[SystemInfo]:
    """Return safe runtime information."""
    settings = get_settings()
    data = SystemInfo(
        name=settings.app.name,
        version=settings.app.version,
        environment=settings.app.environment,
        debug=settings.app.debug,
    )
    return ApiResponse(success=True, data=data)


@router.get("/config", summary="Public configuration")
async def configuration() -> ApiResponse[dict[str, object]]:
    """Return diagnostics-safe configuration without credentials."""
    return ApiResponse(success=True, data=get_settings().public_dict())
