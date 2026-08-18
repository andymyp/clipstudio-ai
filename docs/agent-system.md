# Agent System

The generic agent framework lives under
`apps/backend/app/services/agents/`. It is intentionally independent of video
discovery, transcript extraction, analysis, scoring, rendering, and storage
implementations.

## Runtime flow

An active agent executes one bounded loop:

`Observe -> Analyze -> Decide -> Act -> Evaluate`

The planner creates steps from the configured tool names. The registry resolves
plugins by name, and every tool exposes input/output schemas plus an async
`execute` method. The default discovery, transcript, analysis, scoring,
rendering, and storage tools are safe deferred ports.

## Lifecycle and persistence

`AgentLifecycle` validates transitions across created, configured, inactive,
active, running, paused, stopped, disabled, and archived states. `AgentManager`
connects that runtime to the existing `Agent` and `AgentConfig` tables, emits
typed lifecycle events, and queues work through the bounded async task runner.

## Memory

- `ShortTermMemory` stores current task, context, and decision.
- `LongTermMemory` stores bounded historical results and feedback categories.
- `InMemorySemanticMemory` provides the replaceable async semantic-memory port;
  no vector database is selected or implemented yet.

## Example templates

`templates.example_agents()` provides Funny Moments, Inspirational, and Sad
Story starter configurations. These are examples only; the framework does not
hardcode content categories.
