"""Analysis service contract placeholders."""

from pydantic import BaseModel


class AnalysisServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "analysis"
    ready: bool = False
