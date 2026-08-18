"""Workflow service contract placeholders."""

from pydantic import BaseModel


class WorkflowServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "workflow"
    ready: bool = False
