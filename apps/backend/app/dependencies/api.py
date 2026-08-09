"""FastAPI dependency providers for sessions and local authentication."""

import os
from collections.abc import AsyncIterator
from dataclasses import dataclass

from fastapi import Depends, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.security import LocalTokenValidator
from .container import AppContainer, get_container


@dataclass(frozen=True, slots=True)
class UserContext:
    """Minimal local user context for future authorization policies."""

    subject: str
    permissions: frozenset[str]

    def can(self, permission: str) -> bool:
        """Return whether this context has a permission."""
        return permission in self.permissions


async def get_db_session(
    container: AppContainer = Depends(get_container),
) -> AsyncIterator[AsyncSession]:
    """Provide a transactional request-scoped database session."""
    async with container.database.transaction() as session:
        yield session


async def get_user_context(
    request: Request,
    local_token: str | None = Header(default=None, alias="X-Local-Token"),
) -> UserContext:
    """Validate an optional configured local token without logging it."""
    expected_token = os.getenv("CLIPSTUDIO_LOCAL_TOKEN")
    if expected_token and not LocalTokenValidator(expected_token).validate(
        local_token or ""
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid local token is required.",
        )
    request.state.user = "local"
    return UserContext(
        subject="local",
        permissions=frozenset({"read", "write", "admin"}),
    )
