"""Deterministic metadata normalization before persistence."""

import re

from .schemas import VideoMetadata

_WHITESPACE = re.compile(r"\s+")


def normalize_metadata(metadata: VideoMetadata) -> VideoMetadata:
    """Normalize titles, tags, URL text, and non-negative statistics."""
    title = _WHITESPACE.sub(" ", metadata.title).strip()
    description = (
        _WHITESPACE.sub(" ", metadata.description).strip()
        if metadata.description
        else None
    )
    tags = list(
        dict.fromkeys(tag.strip().casefold() for tag in metadata.tags if tag.strip())
    )
    return metadata.model_copy(
        update={
            "title": title,
            "description": description,
            "tags": tags,
            "view_count": max(0, metadata.view_count),
            "like_count": max(0, metadata.like_count),
        }
    )
