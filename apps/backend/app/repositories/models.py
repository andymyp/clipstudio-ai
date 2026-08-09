"""AI model registry persistence adapter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import AIModel
from .base import BaseRepository


class ModelRepository(BaseRepository[AIModel]):
    """CRUD and provider queries for replaceable model metadata."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, AIModel)

    async def list_available(self) -> list[AIModel]:
        """Return models that can be selected by future services."""
        result = await self.session.execute(
            select(AIModel).where(AIModel.status == "available")
        )
        return list(result.scalars().all())
