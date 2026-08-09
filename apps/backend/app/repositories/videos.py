"""Video-source persistence adapter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import VideoSource
from .base import BaseRepository


class VideoRepository(BaseRepository[VideoSource]):
    """CRUD and duplicate-safe URL queries for video sources."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, VideoSource)

    async def get_by_url(self, url: str) -> VideoSource | None:
        """Return an existing source by canonical URL."""
        result = await self.session.execute(
            select(VideoSource).where(VideoSource.url == url)
        )
        return result.scalar_one_or_none()
