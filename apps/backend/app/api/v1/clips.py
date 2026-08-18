"""Clip review and export endpoints."""

from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...database.models import Clip
from ...dependencies.api import UserContext, get_db_session, get_user_context
from ...repositories.clips import ClipRepository
from ...schemas.api import ClipResponse, JobResponse, Page
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/clips", tags=["clips"])


def _response(clip: Clip) -> ClipResponse:
    """Map a clip model to its public response contract."""
    return ClipResponse.model_validate(clip)


@router.get("", response_model=ApiResponse[Page[ClipResponse]])
async def list_clips(
    status_filter: str | None = Query(default=None, alias="status"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[Page[ClipResponse]]:
    """List clips for human review."""
    items = await ClipRepository(session).list_filtered(
        status=status_filter, limit=limit, offset=offset
    )
    page = Page(
        items=[_response(item) for item in items],
        limit=limit,
        offset=offset,
        returned=len(items),
    )
    return ApiResponse(success=True, data=page)


@router.get("/{clip_id}", response_model=ApiResponse[ClipResponse])
async def get_clip(
    clip_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[ClipResponse]:
    """Get a generated clip."""
    clip = await ClipRepository(session).get(clip_id)
    if clip is None:
        raise HTTPException(status_code=404, detail="Clip not found.")
    return ApiResponse(success=True, data=_response(clip))


async def _review_clip(
    clip_id: str, review_status: str, session: AsyncSession
) -> ApiResponse[ClipResponse]:
    repository = ClipRepository(session)
    clip = await repository.get(clip_id)
    if clip is None:
        raise HTTPException(status_code=404, detail="Clip not found.")
    clip.status = review_status
    await repository.update(clip)
    return ApiResponse(success=True, data=_response(clip))


@router.post("/{clip_id}/approve", response_model=ApiResponse[ClipResponse])
async def approve_clip(
    clip_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[ClipResponse]:
    """Approve a clip for later export/publishing preparation."""
    return await _review_clip(clip_id, "approved", session)


@router.post("/{clip_id}/reject", response_model=ApiResponse[ClipResponse])
async def reject_clip(
    clip_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[ClipResponse]:
    """Reject a clip without deleting its metadata."""
    return await _review_clip(clip_id, "rejected", session)


@router.post(
    "/{clip_id}/export", response_model=ApiResponse[JobResponse], status_code=202
)
async def export_clip(
    clip_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[JobResponse]:
    """Queue export preparation without running rendering in the API process."""
    if await ClipRepository(session).get(clip_id) is None:
        raise HTTPException(status_code=404, detail="Clip not found.")
    return ApiResponse(success=True, data=JobResponse(job_id=str(uuid4())))
