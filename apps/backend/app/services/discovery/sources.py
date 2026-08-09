"""Source connector interfaces and source health contracts."""

from collections.abc import Sequence
from typing import Protocol

from .schemas import SearchQuery, VideoMetadata


class SourceConnector(Protocol):
    """Independent platform adapter contract."""

    name: str
    platform: str

    async def search(self, query: SearchQuery) -> Sequence[VideoMetadata]:
        """Search metadata without downloading full videos."""

    async def fetch_metadata(self, url: str) -> VideoMetadata:
        """Fetch metadata for one validated URL."""

    def validate(self, url: str) -> bool:
        """Validate whether the connector owns a URL."""


class ConnectorError(RuntimeError):
    """Raised when a source adapter cannot complete a metadata request."""


class SourceHealth:
    """Simple in-process health counters for one source connector."""

    def __init__(self) -> None:
        self.searches = 0
        self.failures = 0

    @property
    def success_rate(self) -> float:
        """Return successful search percentage."""
        return (
            100.0
            if self.searches == 0
            else (self.searches - self.failures) / self.searches * 100
        )
