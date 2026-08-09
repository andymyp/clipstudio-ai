"""Generic async repository implementation."""

from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    """CRUD adapter that keeps persistence details out of services."""

    def __init__(self, session: AsyncSession, model: type[ModelT]) -> None:
        self.session = session
        self.model = model

    async def create(self, entity: ModelT) -> ModelT:
        """Stage an entity for insertion."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def get(self, entity_id: object) -> ModelT | None:
        """Read an entity by primary key."""
        return await self.session.get(self.model, entity_id)

    async def list(self, *, limit: int = 100, offset: int = 0) -> Sequence[ModelT]:
        """Return a bounded, deterministic page of entities."""
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def update(self, entity: ModelT) -> ModelT:
        """Stage an existing entity update."""
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity_id: object) -> bool:
        """Delete by primary key and report whether a row was affected."""
        entity = await self.session.get(self.model, entity_id)
        if entity is None:
            return False
        await self.session.delete(entity)
        await self.session.flush()
        return True
