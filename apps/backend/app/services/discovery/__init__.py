"""Metadata-first multi-source discovery engine."""

from .engine import DiscoveryEngine
from .manager import DiscoveryManager
from .schemas import DiscoveryCandidate, SearchQuery, VideoMetadata

__all__ = [
    "DiscoveryCandidate",
    "DiscoveryEngine",
    "DiscoveryManager",
    "SearchQuery",
    "VideoMetadata",
]
