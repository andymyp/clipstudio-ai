"""Rendering service contract placeholders."""

from pydantic import BaseModel


class RenderingServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "rendering"
    ready: bool = False
