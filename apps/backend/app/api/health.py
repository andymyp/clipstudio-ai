"""Health endpoints for process and dependency readiness."""

from typing import TypeVar

from fastapi import APIRouter, Request

from ..core.config import get_settings
from ..database.session import database_health
from ..schemas.common import ApiResponse, HealthData, SystemInfo

router = APIRouter(tags=["system"])
DataT = TypeVar("DataT")


def _success(data: DataT) -> ApiResponse[DataT]:
    return ApiResponse(success=True, data=data)


@router.get(
    "/health", response_model=ApiResponse[HealthData], summary="Application health"
)
async def health() -> ApiResponse[HealthData]:
    """Return application and database readiness."""
    settings = get_settings()
    status = await database_health(settings.database.url)
    data = HealthData(status="ok" if status == "ok" else "degraded", database=status)
    return _success(data)


@router.get(
    "/health/database",
    response_model=ApiResponse[HealthData],
    summary="Database health",
)
async def health_database() -> ApiResponse[HealthData]:
    """Check only the configured database connection."""
    status = await database_health(get_settings().database.url)
    return _success(HealthData(status=status, database=status))


@router.get(
    "/health/system", response_model=ApiResponse[SystemInfo], summary="System health"
)
async def health_system(request: Request) -> ApiResponse[SystemInfo]:
    """Return safe process information and the request correlation id."""
    settings = get_settings()
    data = SystemInfo(
        name=settings.app.name,
        version=settings.app.version,
        environment=settings.app.environment,
        debug=settings.app.debug,
    )
    response = _success(data)
    if request.state.request_id:
        response.message = f"request_id={request.state.request_id}"
    return response
