"""Discovery manager and workflow task adapter."""

from sqlalchemy.ext.asyncio import AsyncSession

from ...core.events import EventBus
from ...services.workflow.tasks import TaskContext, TaskOutput
from .candidates import SemanticDeduplicator
from .connectors import ConnectorRegistry, default_connector_registry
from .engine import DiscoveryEngine
from .schemas import DiscoveryFilters, DiscoveryResult, SearchQuery


class DiscoveryWorkflowTask:
    """Workflow task adapter that searches metadata and returns candidates."""

    name = "discovery"
    description = "Search configured sources and store metadata candidates."
    input_schema = SearchQuery
    output_schema = TaskOutput

    def __init__(self, engine: DiscoveryEngine) -> None:
        self.engine = engine

    async def execute(self, context: TaskContext) -> TaskOutput:
        """Execute a query from workflow task input."""
        query = SearchQuery.model_validate(context.input)
        result = await self.engine.discover(query)
        return TaskOutput(output=result.model_dump(mode="json"))

    async def rollback(self, context: TaskContext, result: TaskOutput) -> None:
        """Discovery stores metadata only; no media side effects need rollback."""


class DiscoveryManager:
    """Dependency-injected facade for manual, scheduled, and workflow discovery."""

    def __init__(
        self,
        *,
        session: AsyncSession,
        event_bus: EventBus,
        connectors: ConnectorRegistry | None = None,
        semantic_deduplicator: SemanticDeduplicator | None = None,
        request_delay_seconds: float = 0,
    ) -> None:
        self.engine = DiscoveryEngine(
            session=session,
            event_bus=event_bus,
            connectors=connectors or default_connector_registry(),
            semantic_deduplicator=semantic_deduplicator,
            request_delay_seconds=request_delay_seconds,
        )

    async def discover(
        self,
        query: SearchQuery,
        *,
        filters: DiscoveryFilters | None = None,
        agent_id: str | None = None,
    ) -> DiscoveryResult:
        """Run a metadata-only discovery search."""
        return await self.engine.discover(query, filters=filters, agent_id=agent_id)

    def workflow_task(self) -> DiscoveryWorkflowTask:
        """Return a plugin suitable for the workflow task registry."""
        return DiscoveryWorkflowTask(self.engine)
