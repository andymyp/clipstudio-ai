"""Example agent templates; production runtime remains category-agnostic."""

from .schemas import AgentConfiguration, AgentGoal


def example_agents() -> dict[str, AgentConfiguration]:
    """Return safe starter profiles for the UI and documentation."""
    return {
        "funny-moments": AgentConfiguration(
            name="Funny Moments Agent",
            category="funny",
            description="Find funny moments suitable for short-form output.",
            goal=AgentGoal(objective="Find viral funny moments"),
            tools=["discovery", "transcript", "analysis", "scoring"],
        ),
        "inspirational": AgentConfiguration(
            name="Inspirational Agent",
            category="motivation",
            description="Find inspirational moments suitable for short-form output.",
            goal=AgentGoal(objective="Find inspirational moments"),
            tools=["discovery", "transcript", "analysis", "scoring"],
        ),
        "sad-story": AgentConfiguration(
            name="Sad Story Agent",
            category="story",
            description="Find emotionally resonant story moments.",
            goal=AgentGoal(objective="Find sad story moments"),
            tools=["discovery", "transcript", "analysis", "scoring"],
        ),
    }
