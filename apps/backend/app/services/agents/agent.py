"""Generic goal-driven agent runtime and decision loop."""

import asyncio
from typing import Any
from uuid import uuid4

from ...core.events import AgentCompleted, AgentFailed, AgentStarted, EventBus
from .evaluator import Evaluator
from .lifecycle import AgentLifecycle
from .memory import InMemorySemanticMemory, LongTermMemory, ShortTermMemory
from .planner import Planner
from .schemas import (
    ActionPlan,
    AgentConfiguration,
    AgentMetrics,
    AgentObservation,
    AgentRunResult,
    AgentState,
)
from .tools import ToolRegistry, default_tool_registry


class Agent:
    """One isolated agent profile, runtime, memory, and decision loop."""

    def __init__(
        self,
        *,
        agent_id: str,
        configuration: AgentConfiguration,
        state: str = AgentState.INACTIVE,
        event_bus: EventBus | None = None,
        tools: ToolRegistry | None = None,
    ) -> None:
        self.agent_id = agent_id
        self.configuration = configuration
        self.lifecycle = AgentLifecycle.from_status(state)
        self.event_bus = event_bus or EventBus()
        self.tools = tools or default_tool_registry()
        self.planner = Planner()
        self.evaluator = Evaluator()
        self.short_term = ShortTermMemory()
        self.long_term = LongTermMemory()
        self.semantic = InMemorySemanticMemory()
        self.metrics = AgentMetrics()

    @property
    def state(self) -> str:
        """Return the current persisted-compatible lifecycle label."""
        return self.lifecycle.state

    def activate(self) -> None:
        """Activate a configured or paused agent."""
        self.lifecycle.transition(AgentState.ACTIVE)

    def pause(self) -> None:
        """Pause an active or running agent before another run."""
        self.lifecycle.transition(AgentState.PAUSED)

    async def observe(self, observation: AgentObservation) -> dict[str, Any]:
        """Record the current task context without interpreting domain content."""
        self.short_term.update(
            task=self.configuration.goal.objective,
            context=observation.data,
        )
        return dict(observation.data)

    async def analyze(self, context: dict[str, Any]) -> dict[str, Any]:
        """Prepare generic decision context for a replaceable planner."""
        return {
            "goal": self.configuration.goal.model_dump(),
            "context": dict(context),
        }

    async def decide(self, analysis: dict[str, Any]) -> ActionPlan:
        """Ask the planner for a bounded tool plan."""
        plan = await self.planner.create_plan(
            self.configuration.goal, self.configuration.tools
        )
        self.short_term.update(
            decision={"analysis": analysis, "plan": plan.model_dump()}
        )
        return plan

    async def act(
        self,
        plan: ActionPlan,
        *,
        cancellation: asyncio.Event | None = None,
    ) -> list[dict[str, Any]]:
        """Execute configured tools with cancellation and step limits."""
        results: list[dict[str, Any]] = []
        for step in plan.steps[: self.configuration.max_steps]:
            if cancellation and cancellation.is_set():
                raise asyncio.CancelledError
            result = await self.tools.execute(step.tool, step.input)
            results.append(result.model_dump())
        return results

    async def evaluate(self, results: list[dict[str, Any]]) -> Any:
        """Evaluate outputs through the replaceable evaluator boundary."""
        return await self.evaluator.evaluate(
            results=results, expected_output=self.configuration.goal.expected_output
        )

    async def run(
        self,
        observation: AgentObservation | None = None,
        *,
        cancellation: asyncio.Event | None = None,
    ) -> AgentRunResult:
        """Run Observe -> Analyze -> Decide -> Act -> Evaluate once."""
        if self.state != AgentState.ACTIVE:
            raise RuntimeError(f"agent must be active to run; state={self.state}")
        self.lifecycle.transition(AgentState.RUNNING)
        run_id = str(uuid4())
        await self.event_bus.publish(
            AgentStarted(agent_id=self.agent_id, run_id=run_id)
        )
        try:
            context = await self.observe(observation or AgentObservation())
            analysis = await self.analyze(context)
            plan = await self.decide(analysis)
            results = await self.act(plan, cancellation=cancellation)
            evaluation = await self.evaluate(results)
            self.metrics.runs += 1
            self.long_term.remember(
                "successful_result" if evaluation.success else "rejected_result",
                {"run_id": run_id, "evaluation": evaluation.model_dump()},
            )
            self.lifecycle.transition(AgentState.ACTIVE)
            result = AgentRunResult(
                run_id=run_id,
                plan=plan,
                results=results,
                evaluation=evaluation,
            )
            await self.event_bus.publish(
                AgentCompleted(agent_id=self.agent_id, run_id=run_id)
            )
            return result
        except BaseException as error:
            if self.state == AgentState.RUNNING:
                self.lifecycle.transition(AgentState.ACTIVE)
            self.long_term.remember(
                "failed_result",
                {"run_id": run_id, "error": type(error).__name__},
            )
            await self.event_bus.publish(
                AgentFailed(
                    agent_id=self.agent_id,
                    run_id=run_id,
                    error=str(error) or type(error).__name__,
                )
            )
            raise


__all__ = ["Agent", "AgentRunResult"]
