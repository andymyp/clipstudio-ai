"""Example workflow definitions for the orchestration layer."""

from .schemas import WorkflowDefinition, WorkflowTaskDefinition


def short_video_production_workflow(agent_id: str | None = None) -> WorkflowDefinition:
    """Return the default deferred short-video pipeline graph."""
    names = (
        "discovery",
        "transcript",
        "analysis",
        "scoring",
        "segment_download",
        "subtitle",
        "rendering",
        "quality_check",
        "storage",
    )
    tasks = [
        WorkflowTaskDefinition(
            name=name,
            task_type=name,
            dependencies=[names[index - 1]] if index else [],
        )
        for index, name in enumerate(names)
    ]
    return WorkflowDefinition(
        name="Short Video Production",
        agent_id=agent_id,
        tasks=tasks,
        max_concurrency=2,
    )


def review_workflow(agent_id: str | None = None) -> WorkflowDefinition:
    """Return a compact example for discover, analyze, generate, and review."""
    return WorkflowDefinition(
        name="Short Video Review",
        agent_id=agent_id,
        tasks=[
            WorkflowTaskDefinition(name="discover", task_type="discovery"),
            WorkflowTaskDefinition(
                name="analyze",
                task_type="analysis",
                dependencies=["discover"],
            ),
            WorkflowTaskDefinition(
                name="generate",
                task_type="rendering",
                dependencies=["analyze"],
            ),
            WorkflowTaskDefinition(
                name="review",
                task_type="quality_check",
                dependencies=["generate"],
            ),
        ],
    )
