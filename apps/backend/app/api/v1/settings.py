"""Safe runtime settings endpoints."""

from fastapi import APIRouter, Depends

from ...core.config import get_settings
from ...dependencies.api import UserContext, get_user_context
from ...schemas.api import SettingsUpdate
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=ApiResponse[dict[str, object]])
async def get_runtime_settings(
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[dict[str, object]]:
    """Return diagnostics-safe runtime settings."""
    return ApiResponse(success=True, data=get_settings().public_dict())


@router.put("", response_model=ApiResponse[dict[str, object]])
async def update_runtime_settings(
    payload: SettingsUpdate,
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[dict[str, object]]:
    """Apply safe settings for the current process."""
    settings = get_settings()
    updates = payload.model_dump(exclude_unset=True)
    if updates:
        settings.app = settings.app.model_copy(update=updates)
    return ApiResponse(
        success=True, data=settings.public_dict(), message="Runtime settings updated."
    )
