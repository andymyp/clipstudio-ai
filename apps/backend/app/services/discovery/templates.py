"""Example discovery-agent configurations."""

from .schemas import DiscoveryFilters, SearchQuery


def funny_moments_query() -> tuple[SearchQuery, DiscoveryFilters]:
    """Return an offline-safe Funny Moments discovery example."""
    return (
        SearchQuery(
            keywords=["funny", "interview", "moments"],
            category="funny",
            topic="viral moments",
            platforms=["youtube"],
            limit=20,
        ),
        DiscoveryFilters(min_duration=10, max_duration=180),
    )
