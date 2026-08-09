"""Agent memory ports and bounded local implementations."""

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class ShortTermMemory:
    """Current workflow context for one running agent."""

    current_task: str | None = None
    context: dict[str, Any] = field(default_factory=dict)
    current_decision: dict[str, Any] | None = None

    def update(
        self,
        *,
        task: str | None = None,
        context: dict[str, Any] | None = None,
        decision: dict[str, Any] | None = None,
    ) -> None:
        """Replace only the supplied short-term fields."""
        if task is not None:
            self.current_task = task
        if context is not None:
            self.context = dict(context)
        if decision is not None:
            self.current_decision = dict(decision)

    def snapshot(self) -> dict[str, Any]:
        """Return a detached context snapshot."""
        return {
            "current_task": self.current_task,
            "context": dict(self.context),
            "current_decision": self.current_decision,
        }


@dataclass(slots=True)
class MemoryRecord:
    """One historical result or feedback item."""

    kind: str
    content: dict[str, Any]


@dataclass(slots=True)
class LongTermMemory:
    """Bounded historical memory for decisions and content outcomes."""

    max_records: int = 1000
    records: list[MemoryRecord] = field(default_factory=list)

    def remember(self, kind: str, content: dict[str, Any]) -> None:
        """Append a bounded historical record."""
        if self.max_records < 1:
            raise ValueError("max_records must be positive")
        self.records.append(MemoryRecord(kind=kind, content=dict(content)))
        del self.records[: max(0, len(self.records) - self.max_records)]

    def by_kind(self, kind: str) -> list[MemoryRecord]:
        """Return records matching a semantic category."""
        return [record for record in self.records if record.kind == kind]


class SemanticMemory(Protocol):
    """Future vector-backed semantic memory interface."""

    async def store(self, content: dict[str, Any]) -> str:
        """Store content and return an opaque memory identifier."""

    async def search(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        """Search semantically related content."""


@dataclass(slots=True)
class InMemorySemanticMemory:
    """Deterministic placeholder until a vector store is selected."""

    entries: dict[str, dict[str, Any]] = field(default_factory=dict)

    async def store(self, content: dict[str, Any]) -> str:
        """Store a detached record without pretending to provide embeddings."""
        key = f"memory-{len(self.entries) + 1}"
        self.entries[key] = dict(content)
        return key

    async def search(self, query: str, *, limit: int = 10) -> list[dict[str, Any]]:
        """Return simple lexical matches as a testable pre-vector adapter."""
        needle = query.casefold()
        matches = [
            value for value in self.entries.values() if needle in repr(value).casefold()
        ]
        return matches[:limit]
