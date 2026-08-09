"""Clip persistence adapter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Clip
from .base import BaseRepository


class ClipRepository(BaseRepository[Clip]):
    """CRUD and review-status queries for generated clips."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Clip)

    async def list_by_status(self, status: str, *, limit: int = 100) -> list[Clip]:
        """Return clips requiring a particular review state."""
        result = await self.session.execute(
            select(Clip).where(Clip.status == status).limit(limit)
        )
        return list(result.scalars().all())

    async def list_filtered(
        self, *, status: str | None = None, limit: int = 100, offset: int = 0
    ) -> list[Clip]:
        """Return a bounded clip page, optionally filtered by status."""
        statement = select(Clip)
        if status:
            statement = statement.where(Clip.status == status)
        result = await self.session.execute(statement.offset(offset).limit(limit))
        return list(result.scalars().all())
