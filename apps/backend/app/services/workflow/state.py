"""Workflow and task state machines."""

from dataclasses import dataclass

from .schemas import TaskState, WorkflowState


class InvalidWorkflowTransition(ValueError):
    """Raised for an invalid workflow or task state transition."""


_WORKFLOW_TRANSITIONS: dict[WorkflowState, frozenset[WorkflowState]] = {
    WorkflowState.CREATED: frozenset({WorkflowState.QUEUED, WorkflowState.RUNNING}),
    WorkflowState.QUEUED: frozenset(
        {WorkflowState.RUNNING, WorkflowState.PAUSED, WorkflowState.CANCELLED}
    ),
    WorkflowState.RUNNING: frozenset(
        {
            WorkflowState.PAUSED,
            WorkflowState.COMPLETED,
            WorkflowState.FAILED,
            WorkflowState.CANCELLED,
        }
    ),
    WorkflowState.PAUSED: frozenset(
        {WorkflowState.QUEUED, WorkflowState.RUNNING, WorkflowState.CANCELLED}
    ),
    WorkflowState.COMPLETED: frozenset(),
    WorkflowState.FAILED: frozenset({WorkflowState.QUEUED}),
    WorkflowState.CANCELLED: frozenset(),
}

_TASK_TRANSITIONS: dict[TaskState, frozenset[TaskState]] = {
    TaskState.PENDING: frozenset(
        {TaskState.RUNNING, TaskState.CANCELLED, TaskState.SKIPPED}
    ),
    TaskState.RUNNING: frozenset(
        {TaskState.SUCCESS, TaskState.FAILED, TaskState.RETRYING, TaskState.CANCELLED}
    ),
    TaskState.RETRYING: frozenset(
        {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED}
    ),
    TaskState.SUCCESS: frozenset(),
    TaskState.FAILED: frozenset({TaskState.RETRYING}),
    TaskState.CANCELLED: frozenset(),
    TaskState.SKIPPED: frozenset(),
}


@dataclass(slots=True)
class WorkflowLifecycle:
    """Explicit state machine for workflow instances."""

    state: WorkflowState = WorkflowState.CREATED

    def transition(self, target: WorkflowState) -> WorkflowState:
        """Move to a permitted workflow state."""
        if target == self.state:
            return self.state
        if target not in _WORKFLOW_TRANSITIONS[self.state]:
            raise InvalidWorkflowTransition(
                f"cannot transition {self.state} -> {target}"
            )
        self.state = target
        return self.state


@dataclass(slots=True)
class TaskLifecycle:
    """Explicit state machine for individual workflow tasks."""

    state: TaskState = TaskState.PENDING

    def transition(self, target: TaskState) -> TaskState:
        """Move to a permitted task state."""
        if target == self.state:
            return self.state
        if target not in _TASK_TRANSITIONS[self.state]:
            raise InvalidWorkflowTransition(
                f"cannot transition {self.state} -> {target}"
            )
        self.state = target
        return self.state
