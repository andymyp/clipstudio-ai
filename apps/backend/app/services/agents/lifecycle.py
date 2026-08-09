"""Agent lifecycle state machine."""

from dataclasses import dataclass

from .schemas import AgentState


class InvalidAgentTransition(ValueError):
    """Raised when a lifecycle transition is not permitted."""


_TRANSITIONS: dict[str, frozenset[str]] = {
    AgentState.CREATED: frozenset({AgentState.CONFIGURED, AgentState.ACTIVE}),
    AgentState.CONFIGURED: frozenset({AgentState.ACTIVE, AgentState.INACTIVE}),
    AgentState.INACTIVE: frozenset({AgentState.CONFIGURED, AgentState.ACTIVE}),
    AgentState.ACTIVE: frozenset(
        {AgentState.RUNNING, AgentState.PAUSED, AgentState.STOPPED, AgentState.DISABLED}
    ),
    AgentState.RUNNING: frozenset(
        {AgentState.ACTIVE, AgentState.PAUSED, AgentState.STOPPED}
    ),
    AgentState.PAUSED: frozenset({AgentState.ACTIVE, AgentState.STOPPED}),
    AgentState.STOPPED: frozenset({AgentState.ACTIVE, AgentState.ARCHIVED}),
    AgentState.DISABLED: frozenset({AgentState.ACTIVE, AgentState.ARCHIVED}),
    AgentState.ARCHIVED: frozenset(),
}


@dataclass(slots=True)
class AgentLifecycle:
    """Small explicit state machine that prevents unsafe transitions."""

    state: str = AgentState.CREATED

    def transition(self, target: str) -> str:
        """Move to a permitted state and return the new state."""
        if target == self.state:
            return self.state
        allowed = _TRANSITIONS.get(self.state, frozenset())
        if target not in allowed:
            raise InvalidAgentTransition(f"cannot transition {self.state} -> {target}")
        self.state = target
        return self.state

    @classmethod
    def from_status(cls, status: str | None) -> "AgentLifecycle":
        """Create a lifecycle from a persisted status with safe fallback."""
        current = status or AgentState.CREATED
        if current not in _TRANSITIONS:
            raise InvalidAgentTransition(f"unknown agent state: {current}")
        return cls(current)
