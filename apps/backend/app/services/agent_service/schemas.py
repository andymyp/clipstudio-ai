"""Agent service contract placeholders."""

from pydantic import BaseModel


class AgentServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "agent"
    ready: bool = False
