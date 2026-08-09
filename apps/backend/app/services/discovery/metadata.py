"""Metadata parsing and safe field coercion."""

from typing import Any

from .schemas import VideoMetadata


def parse_metadata(payload: dict[str, Any], *, platform: str) -> VideoMetadata:
    """Parse connector payloads into the normalized metadata contract."""
    value = dict(payload)
    value.setdefault("platform", platform)
    return VideoMetadata.model_validate(value)
