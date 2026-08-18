"""Discovery service contract placeholders."""

from pydantic import BaseModel


class DiscoveryServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "discovery"
    ready: bool = False
