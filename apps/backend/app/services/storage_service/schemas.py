"""Storage service contract placeholders."""

from pydantic import BaseModel


class StorageServiceStatus(BaseModel):
    """Non-business status contract for skeleton health checks."""

    service: str = "storage"
    ready: bool = False
