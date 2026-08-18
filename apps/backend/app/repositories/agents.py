"""Agent persistence adapter."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..database.models import Agent
from .base import BaseRepository


class AgentRepository(BaseRepository[Agent]):
    """CRUD and status queries for agents."""

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Agent)

    async def list_active(self) -> list[Agent]:
        """Return active agents for future orchestration."""
        result = await self.session.execute(
            select(Agent).where(Agent.status == "active")
        )
        return list(result.scalars().all())

    async def get_with_config(self, agent_id: str) -> Agent | None:
        """Load an agent together with its optional configuration row."""
        result = await self.session.execute(
            select(Agent)
            .options(selectinload(Agent.config))
            .where(Agent.id == agent_id)
        )
        return result.scalar_one_or_none()
