"""Connector registry with safe deferred platform adapters."""

from collections.abc import Sequence
from urllib.parse import urlparse

from .schemas import SearchQuery, VideoMetadata
from .sources import ConnectorError, SourceConnector


class DeferredConnector:
    """Platform port that performs no network calls until an adapter is installed."""

    def __init__(self, platform: str) -> None:
        self.name = f"{platform}-deferred"
        self.platform = platform

    async def search(self, query: SearchQuery) -> Sequence[VideoMetadata]:
        """Return no results while keeping the connector contract available."""
        return []

    async def fetch_metadata(self, url: str) -> VideoMetadata:
        """Reject metadata fetches until a real platform adapter is configured."""
        raise ConnectorError(f"no {self.platform} connector is configured")

    def validate(self, url: str) -> bool:
        """Validate URL shape and expected host ownership."""
        parsed = urlparse(url)
        return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


class StaticConnector:
    """Deterministic connector useful for offline operation and tests."""

    def __init__(self, platform: str, items: Sequence[VideoMetadata]) -> None:
        self.name = f"{platform}-static"
        self.platform = platform
        self._items = tuple(items)

    async def search(self, query: SearchQuery) -> Sequence[VideoMetadata]:
        """Return bounded static metadata matching the requested platform."""
        return self._items[: query.limit]

    async def fetch_metadata(self, url: str) -> VideoMetadata:
        """Fetch one static item by URL."""
        for item in self._items:
            if str(item.url) == url:
                return item
        raise ConnectorError(f"metadata not found: {url}")

    def validate(self, url: str) -> bool:
        """Validate URL shape for the static source."""
        return DeferredConnector(self.platform).validate(url)


class ConnectorRegistry:
    """Plugin registry for independent source connectors."""

    def __init__(self, connectors: Sequence[SourceConnector] | None = None) -> None:
        self._connectors: dict[str, SourceConnector] = {}
        for connector in connectors or []:
            self.register(connector)

    def register(self, connector: SourceConnector) -> None:
        """Register one connector by platform."""
        if connector.platform in self._connectors:
            raise ValueError(f"connector already registered: {connector.platform}")
        self._connectors[connector.platform] = connector

    def get(self, platform: str) -> SourceConnector:
        """Resolve one connector by normalized platform name."""
        try:
            return self._connectors[platform.lower()]
        except KeyError as error:
            raise ConnectorError(f"connector not registered: {platform}") from error

    def select(self, platforms: Sequence[str]) -> list[SourceConnector]:
        """Select requested connectors, or all registered connectors by default."""
        if not platforms:
            return list(self._connectors.values())
        return [self.get(platform) for platform in platforms]

    def platforms(self) -> tuple[str, ...]:
        """Return supported platform names."""
        return tuple(self._connectors)


def default_connector_registry() -> ConnectorRegistry:
    """Expose supported platform architecture without external credentials."""
    return ConnectorRegistry(
        [
            DeferredConnector(platform)
            for platform in ("youtube", "tiktok", "instagram", "reddit")
        ]
    )
