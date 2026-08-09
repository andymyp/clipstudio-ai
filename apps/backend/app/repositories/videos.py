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

    async def get_by_content_hash(self, content_hash: str) -> VideoSource | None:
        """Return a source with an exact content hash when one exists."""
        result = await self.session.execute(
            select(VideoSource).where(VideoSource.content_hash == content_hash)
        )
        return result.scalar_one_or_none()

    async def list_filtered(
        self,
        *,
        platform: str | None = None,
        status: str | None = None,
        search: str | None = None,
        limit: int = 100,
        offset: int = 0,
    ) -> list[VideoSource]:
        """Return a bounded filtered source page."""
        statement = select(VideoSource)
        if platform:
            statement = statement.where(VideoSource.platform == platform)
        if status:
            statement = statement.where(VideoSource.status == status)
        if search:
            statement = statement.where(VideoSource.title.ilike(f"%{search}%"))
        result = await self.session.execute(statement.offset(offset).limit(limit))
        return list(result.scalars().all())
