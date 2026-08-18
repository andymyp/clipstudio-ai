"""Cheap metadata filters applied before any media download."""

from .schemas import DiscoveryFilters, VideoMetadata


def filter_reason(metadata: VideoMetadata, rules: DiscoveryFilters) -> str | None:
    """Return the first filter reason, or ``None`` when accepted."""
    if rules.min_duration is not None and (
        metadata.duration is None or metadata.duration < rules.min_duration
    ):
        return "duration_below_minimum"
    if rules.max_duration is not None and (
        metadata.duration is not None and metadata.duration > rules.max_duration
    ):
        return "duration_above_maximum"
    if rules.language and metadata.language != rules.language:
        return "language_mismatch"
    if rules.min_quality_score is not None and (
        metadata.quality_score is None
        or metadata.quality_score < rules.min_quality_score
    ):
        return "quality_below_minimum"
    if rules.min_view_count is not None and metadata.view_count < rules.min_view_count:
        return "popularity_below_minimum"
    return None


def rank_score(metadata: VideoMetadata, query_text: str) -> float:
    """Compute a transparent metadata-only relevance score."""
    haystack = f"{metadata.title} {metadata.description or ''}".casefold()
    keywords = [word for word in query_text.casefold().split() if word]
    keyword_score = min(50.0, sum(10.0 for word in keywords if word in haystack))
    popularity_score = min(30.0, metadata.view_count / 100_000)
    quality_score = metadata.quality_score * 0.2 if metadata.quality_score else 0
    return min(100.0, keyword_score + popularity_score + quality_score)
