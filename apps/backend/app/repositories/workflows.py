"""Workflow persistence adapter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import Workflow
from .base import BaseRepository


class WorkflowRepository(BaseRepository[Workflow]):
    """CRUD and status queries for workflow state."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Workflow)

    async def list_pending(self, *, limit: int = 100) -> list[Workflow]:
        """Return pending workflows in creation order."""
        result = await self.session.execute(
            select(Workflow).where(Workflow.status == "pending").limit(limit)
        )
        return list(result.scalars().all())

    async def list_filtered(
        self, *, status: str | None = None, limit: int = 100, offset: int = 0
    ) -> list[Workflow]:
        """Return a bounded workflow page, optionally filtered by status."""
        statement = select(Workflow)
        if status:
            statement = statement.where(Workflow.status == status)
        result = await self.session.execute(statement.offset(offset).limit(limit))
        return list(result.scalars().all())
