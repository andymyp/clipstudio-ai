"""Video source management endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ...dependencies.api import UserContext, get_db_session, get_user_context
from ...repositories.videos import VideoRepository
from ...schemas.api import Page, VideoResponse
from ...schemas.common import ApiResponse

router = APIRouter(prefix="/videos", tags=["videos"])


@router.get("", response_model=ApiResponse[Page[VideoResponse]])
async def list_videos(
    platform: str | None = Query(default=None),
    status: str | None = Query(default=None),
    search: str | None = Query(default=None, max_length=200),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[Page[VideoResponse]]:
    """List sources with optional platform/status/title filtering."""
    items = await VideoRepository(session).list_filtered(
        platform=platform, status=status, search=search, limit=limit, offset=offset
    )
    page = Page(
        items=[VideoResponse.model_validate(item) for item in items],
        limit=limit,
        offset=offset,
        returned=len(items),
    )
    return ApiResponse(success=True, data=page)


@router.get("/{video_id}", response_model=ApiResponse[VideoResponse])
async def get_video(
    video_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[VideoResponse]:
    """Get a source by id."""
    video = await VideoRepository(session).get(video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video source not found.")
    return ApiResponse(success=True, data=VideoResponse.model_validate(video))


@router.delete("/{video_id}", response_model=ApiResponse[dict[str, bool]])
async def delete_video(
    video_id: str,
    session: AsyncSession = Depends(get_db_session),
    _: UserContext = Depends(get_user_context),
) -> ApiResponse[dict[str, bool]]:
    """Delete source metadata; media files are managed by storage services."""
    deleted = await VideoRepository(session).delete(video_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Video source not found.")
    return ApiResponse(success=True, data={"deleted": True})
