"""Application exception taxonomy."""


class ClipStudioError(Exception):
    """Base class for expected application failures."""

    code = "clipstudio_error"

    def __init__(self, message: str, *, recovery: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.recovery = recovery


class ValidationError(ClipStudioError):
    """Raised when input fails domain validation."""

    code = "validation_error"


class ProcessingError(ClipStudioError):
    """Raised when a pipeline operation cannot complete."""

    code = "processing_error"


class ModelError(ClipStudioError):
    """Raised when an AI model adapter fails."""

    code = "model_error"


class StorageError(ClipStudioError):
    """Raised when persistent or runtime storage fails."""

    code = "storage_error"
