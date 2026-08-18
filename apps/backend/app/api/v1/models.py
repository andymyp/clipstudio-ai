"""AI model registry endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependencies.api import UserContext, get_db_session, get_user_context
from ...repositories.models import ModelRepository
from ...schemas.api import ModelResponse
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/models", tags=["models"])


@router.get("", response_model=ApiResponse[list[ModelResponse]])
async def list_models(
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[list[ModelResponse]]:
    """List registered AI models."""
    items = await ModelRepository(session).list(limit=100)
    return ApiResponse(
        success=True,
        data=[ModelResponse.model_validate(item) for item in items],
    )


@router.get("/{model_id}", response_model=ApiResponse[ModelResponse])
async def get_model(
    model_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[ModelResponse]:
    """Get a registered model."""
    model = await ModelRepository(session).get(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    return ApiResponse(success=True, data=ModelResponse.model_validate(model))


@router.post("/{model_id}/activate", response_model=ApiResponse[ModelResponse])
async def activate_model(
    model_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[ModelResponse]:
    """Mark a model available for future selection."""
    repository = ModelRepository(session)
    model = await repository.get(model_id)
    if model is None:
        raise HTTPException(status_code=404, detail="Model not found.")
    model.status = "active"
    await repository.update(model)
    return ApiResponse(success=True, data=ModelResponse.model_validate(model))
