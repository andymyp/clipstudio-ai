"""Idempotent development seed data."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import AIModel


async def seed_defaults(session: AsyncSession) -> None:
    """Insert safe local model defaults without credentials or user data."""
    result = await session.execute(select(AIModel).where(AIModel.name == "disabled"))
    if result.scalar_one_or_none() is None:
        session.add(
            AIModel(
                name="disabled",
                provider="local",
                type="llm",
                version="none",
                status="available",
            )
        )
        await session.flush()
