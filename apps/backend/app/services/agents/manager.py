"""Persistence-aware agent manager and asynchronous execution adapter."""

from collections.abc import Callable
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ...core.events import AgentActivated, AgentCreated, EventBus
from ...database.models import Agent as AgentModel
from ...database.models import AgentConfig
from ...repositories.agents import AgentRepository
from ...schemas.entities import AgentCreate
from ...tasks.base import AsyncTaskRunner
from .agent import Agent
from .lifecycle import InvalidAgentTransition
from .schemas import (
    AgentConfiguration,
    AgentGoal,
    AgentMonitor,
    AgentObservation,
    AgentRunResult,
    AgentState,
)
from .tools import ToolRegistry, default_tool_registry


class AgentNotFoundError(LookupError):
    """Raised when an agent id is not persisted."""


class AgentOperationError(ValueError):
    """Raised when an agent cannot perform a requested operation."""


ToolRegistryFactory = Callable[[], ToolRegistry]


class AgentManager:
    """Coordinate persistence, lifecycle transitions, runtime, and events."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        session_factory: async_sessionmaker[AsyncSession],
        event_bus: EventBus,
        task_runner: AsyncTaskRunner,
        tools_factory: ToolRegistryFactory = default_tool_registry,
    ) -> None:
        self.session = session
        self.session_factory = session_factory
        self.event_bus = event_bus
        self.task_runner = task_runner
        self.tools_factory = tools_factory
        self._runtimes: dict[str, Agent] = {}

    @staticmethod
    def configuration_from_model(agent: AgentModel) -> AgentConfiguration:
        """Map persisted agent/config rows into the generic runtime contract."""
        stored = agent.configuration or {}
        goal_value = stored.get("goal")
        goal = (
            AgentGoal.model_validate(goal_value)
            if isinstance(goal_value, dict)
            else AgentGoal(
                objective=agent.description or f"Process {agent.category} content."
            )
        )
        config = agent.config
        return AgentConfiguration(
            name=agent.name,
            category=agent.category,
            description=agent.description,
            goal=goal,
            sources=list(config.sources) if config else list(stored.get("sources", [])),
            prompt=config.prompt if config else stored.get("prompt"),
            model=(
                dict(config.model_settings) if config else dict(stored.get("model", {}))
            ),
            schedule=dict(agent.schedule or {}),
            watermark=dict(agent.watermark or {}),
            scoring_rules=(
                dict(config.scoring_rules)
                if config
                else dict(stored.get("scoring_rules", {}))
            ),
            tools=list(stored.get("tools", [])),
            max_steps=int(stored.get("max_steps", 10)),
        )

    async def _load(self, agent_id: str) -> AgentModel:
        agent = await AgentRepository(self.session).get_with_config(agent_id)
        if agent is None:
            raise AgentNotFoundError(f"agent not found: {agent_id}")
        return agent

    def _runtime(self, model: AgentModel) -> Agent:
        runtime = Agent(
            agent_id=model.id,
            configuration=self.configuration_from_model(model),
            state=model.status,
            event_bus=self.event_bus,
            tools=self.tools_factory(),
        )
        self._runtimes[model.id] = runtime
        return runtime

    async def create(self, payload: AgentCreate) -> AgentModel:
        """Persist an agent profile and its normalized configuration row."""
        goal_value = payload.configuration.get("goal")
        goal = (
            AgentGoal.model_validate(goal_value)
            if isinstance(goal_value, dict)
            else AgentGoal(
                objective=payload.description or f"Process {payload.category} content."
            )
        )
        configuration = dict(payload.configuration)
        configuration["goal"] = goal.model_dump()
        configuration.setdefault("tools", [])
        configuration.setdefault("max_steps", 10)
        agent = await AgentRepository(self.session).create(
            AgentModel(
                name=payload.name,
                category=payload.category,
                description=payload.description,
                status=AgentState.INACTIVE,
                configuration=configuration,
                schedule=dict(payload.schedule),
                watermark=dict(payload.watermark),
            )
        )
        self.session.add(
            AgentConfig(
                agent_id=agent.id,
                sources=list(configuration.get("sources", [])),
                prompt=configuration.get("prompt"),
                model_settings=dict(configuration.get("model", {})),
                scoring_rules=dict(configuration.get("scoring_rules", {})),
            )
        )
        await self.session.flush()
        await self.event_bus.publish(AgentCreated(agent_id=agent.id))
        return agent

    async def activate(self, agent_id: str) -> AgentModel:
        """Validate configuration, persist active state, and publish an event."""
        model = await self._load(agent_id)
        runtime = self._runtime(model)
        try:
            runtime.activate()
        except (InvalidAgentTransition, ValueError) as error:
            raise AgentOperationError(str(error)) from error
        model.status = runtime.state
        await AgentRepository(self.session).update(model)
        await self.event_bus.publish(AgentActivated(agent_id=agent_id))
        return model

    async def pause(self, agent_id: str) -> AgentModel:
        """Persist a paused state for an active or running agent."""
        model = await self._load(agent_id)
        runtime = self._runtime(model)
        try:
            runtime.pause()
        except (InvalidAgentTransition, ValueError) as error:
            raise AgentOperationError(str(error)) from error
        model.status = runtime.state
        await AgentRepository(self.session).update(model)
        return model

    async def delete(self, agent_id: str) -> bool:
        """Delete a persisted agent definition and isolate its runtime cache."""
        deleted = await AgentRepository(self.session).delete(agent_id)
        if not deleted:
            raise AgentNotFoundError(f"agent not found: {agent_id}")
        self._runtimes.pop(agent_id, None)
        return True

    async def execute(
        self,
        agent_id: str,
        observation: AgentObservation | None = None,
    ) -> AgentRunResult:
        """Execute one run synchronously for deterministic callers and tests."""
        model = await self._load(agent_id)
        runtime = self._runtimes.get(agent_id) or self._runtime(model)
        if runtime.state != AgentState.ACTIVE:
            raise AgentOperationError(
                f"agent must be active to run; state={runtime.state}"
            )
        result = await runtime.run(observation)
        model.status = runtime.state
        await AgentRepository(self.session).update(model)
        return result

    async def enqueue(
        self,
        agent_id: str,
        observation: AgentObservation | None = None,
    ) -> str:
        """Queue a bounded asynchronous run using a fresh worker session."""
        model = await self._load(agent_id)
        runtime = self._runtimes.get(agent_id) or self._runtime(model)
        if runtime.state not in {AgentState.ACTIVE, AgentState.PAUSED}:
            raise AgentOperationError(
                f"agent must be active to run; state={runtime.state}"
            )
        job_id = str(uuid4())
        configuration = runtime.configuration.model_copy(deep=True)

        async def operation() -> None:
            async with self.session_factory() as worker_session:
                repository = AgentRepository(worker_session)
                worker_model = await repository.get_with_config(agent_id)
                if worker_model is None:
                    return
                worker_model.status = AgentState.RUNNING
                await worker_session.commit()
                worker_runtime = Agent(
                    agent_id=agent_id,
                    configuration=configuration,
                    state=AgentState.ACTIVE,
                    event_bus=self.event_bus,
                    tools=self.tools_factory(),
                )
                try:
                    await worker_runtime.run(observation)
                except BaseException:
                    worker_model = await repository.get(agent_id)
                    if worker_model is not None:
                        worker_model.status = AgentState.ACTIVE
                        await repository.update(worker_model)
                    await worker_session.commit()
                    raise
                worker_model = await repository.get(agent_id)
                if worker_model is not None:
                    worker_model.status = (
                        AgentState.PAUSED
                        if worker_model.status == AgentState.PAUSED
                        else AgentState.ACTIVE
                    )
                    await repository.update(worker_model)
                await worker_session.commit()

        try:
            self.task_runner.submit(operation)
        except RuntimeError as error:
            raise AgentOperationError(str(error)) from error
        return job_id

    async def monitor(self, agent_id: str) -> AgentMonitor:
        """Return lifecycle and runtime counters for one agent."""
        model = await self._load(agent_id)
        runtime = self._runtimes.get(agent_id) or self._runtime(model)
        return AgentMonitor(
            agent_id=agent_id,
            state=model.status,
            active_tasks=self.task_runner.active_count,
            metrics=runtime.metrics,
        )
