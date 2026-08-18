"""Generic goal-to-action planner."""

from .schemas import ActionPlan, AgentGoal, PlanStep


class Planner:
    """Create bounded plans from configuration-selected tool plugins."""

    async def create_plan(self, goal: AgentGoal, tool_names: list[str]) -> ActionPlan:
        """Create one action per configured tool in deterministic order."""
        steps = [
            PlanStep(
                name=f"step-{index}",
                tool=tool_name,
                input={"objective": goal.objective},
            )
            for index, tool_name in enumerate(tool_names, start=1)
        ]
        return ActionPlan(objective=goal.objective, steps=steps)
