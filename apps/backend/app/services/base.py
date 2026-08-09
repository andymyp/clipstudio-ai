"""Base application service contract."""

from logging import Logger
from typing import Any

from ..core.config import Settings


class BaseService:
    """Dependency-injected home for application business rules."""

    def __init__(
        self,
        *,
        settings: Settings,
        logger: Logger,
        external_clients: dict[str, Any] | None = None,
    ) -> None:
        self.settings = settings
        self.logger = logger
        self.external_clients = external_clients or {}
