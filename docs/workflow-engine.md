# Workflow Engine

The workflow engine lives under `apps/backend/app/services/workflow/` and
coordinates independent task plugins without implementing discovery, AI
analysis, or rendering.

## Execution model

Workflow definitions are persisted as instances containing named tasks,
dependencies, inputs, retry limits, and concurrency limits. The executor
validates the task graph, runs dependency-ready tasks sequentially or in
bounded parallel batches, and records progress after each successful task.

The default short-video template exposes deferred ports for discovery,
transcript, analysis, scoring, segment download, subtitles, rendering, quality
checks, and storage.

## Reliability

Each task has a state machine and exponential retry policy. Workflow and task
state, attempts, errors, and outputs are persisted. Queue submission uses the
shared resource-limited async runner; pause, resume, and cancel use shared
cancellation signals. The workflow event bus publishes creation, start,
task-start, task-completed, task-failed, completion, and failure events.

## Database migration

Migration `7a4f63e29b11_workflow_engine_fields` adds workflow definitions/errors
and task input, dependency, attempt, and max-attempt fields. The local database
is currently at this migration head.
