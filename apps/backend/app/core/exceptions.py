"""Application exception exports and API-safe error types."""

from backend.app.core.exceptions import (
    ClipStudioError,
    ModelError,
    ProcessingError,
    StorageError,
    ValidationError,
)


class ApplicationError(ClipStudioError):
    """Raised for expected application-layer failures."""

    code = "application_error"


__all__ = [
    "ApplicationError",
    "ClipStudioError",
    "ModelError",
    "ProcessingError",
    "StorageError",
    "ValidationError",
]
