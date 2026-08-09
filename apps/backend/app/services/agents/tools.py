"""Plugin-style agent tool contracts and safe placeholder tools."""

from collections.abc import Awaitable, Callable
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field


class ToolPayload(BaseModel):
    """Generic input schema accepted by replaceable tools."""

    model_config = ConfigDict(extra="allow")

    data: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    """Generic output schema returned by every tool."""

    tool: str
    status: str
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None


class AgentTool(Protocol):
    """Tool interface used by planners and agent runtimes."""

    name: str
    description: str
    input_schema: type[BaseModel]
    output_schema: type[ToolResult]

    async def execute(self, payload: dict[str, Any]) -> ToolResult:
        """Execute a tool action asynchronously."""


ToolHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


class FunctionTool:
    """Adapter for an independently implemented async tool function."""

    input_schema: type[BaseModel] = ToolPayload
    output_schema: type[ToolResult] = ToolResult

    def __init__(self, name: str, description: str, handler: ToolHandler) -> None:
        self.name = name
        self.description = description
        self._handler = handler

    async def execute(self, payload: dict[str, Any]) -> ToolResult:
        """Validate input, invoke the handler, and normalize output."""
        validated = self.input_schema.model_validate(payload)
        output = await self._handler(validated.model_dump())
        return self.output_schema(tool=self.name, status="completed", output=output)


class DeferredTool(FunctionTool):
    """Safe port for a future domain tool; performs no media/AI work."""

    def __init__(self, name: str, description: str) -> None:
        async def deferred(payload: dict[str, Any]) -> dict[str, Any]:
            return {"accepted": True, "input": payload}

        super().__init__(name, description, deferred)


class ToolRegistry:
    """Runtime registry that supports plugins without category conditionals."""

    def __init__(self, tools: list[AgentTool] | None = None) -> None:
        self._tools: dict[str, AgentTool] = {}
        for tool in tools or []:
            self.register(tool)

    def register(self, tool: AgentTool) -> None:
        """Register a uniquely named tool plugin."""
        if tool.name in self._tools:
            raise ValueError(f"tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> AgentTool:
        """Resolve a registered tool or raise a clear configuration error."""
        try:
            return self._tools[name]
        except KeyError as error:
            raise KeyError(f"tool not registered: {name}") from error

    def names(self) -> tuple[str, ...]:
        """Return available tool names in registration order."""
        return tuple(self._tools)

    async def execute(self, name: str, payload: dict[str, Any]) -> ToolResult:
        """Execute one named plugin."""
        return await self.get(name).execute(payload)


def default_tool_registry() -> ToolRegistry:
    """Build ports for future processing services without implementing them."""
    descriptions = {
        "discovery": "Discover candidate content through a later service.",
        "transcript": "Acquire transcript data through a later service.",
        "analysis": "Analyze content through a later service.",
        "scoring": "Score candidate content through a later service.",
        "rendering": "Render clips through a later service.",
        "storage": "Persist outputs through a later service.",
    }
    return ToolRegistry(
        [DeferredTool(name, description) for name, description in descriptions.items()]
    )
