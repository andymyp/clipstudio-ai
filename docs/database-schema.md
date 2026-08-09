# Database Schema

ClipStudio AI uses SQLite as its local-first operational database. SQLAlchemy
and Alembic keep the metadata portable so a future explicitly configured
server deployment can use a compatible async relational backend. JSON columns
are used instead of PostgreSQL-only JSONB to preserve local SQLite support.

## Tables

| Table | Purpose |
| --- | --- |
| `agents` | Agent identity, lifecycle status, and high-level configuration |
| `agent_configs` | Agent sources, prompt, model settings, scoring, and one-to-one configuration |
| `video_sources` | Discovered source metadata, URL uniqueness, and content hash |
| `transcripts` | Transcript text, segments, language, and timestamps |
| `video_analysis` | Structured analysis scores and AI result payload |
| `workflows` | Workflow execution status, current step, and progress |
| `workflow_tasks` | Resumable task status, result, and error state |
| `clips` | Generated clip artifact metadata and review status |
| `clip_metadata` | Platform-specific title, description, hashtags, and platform |
| `ai_models` | Replaceable model provider/type/version registry |
| `processing_history` | Traceable actions, events, and structured results |

Every entity has a string UUID `id`, `created_at`, and `updated_at`. Timestamps
are UTC-aware. Media bytes are not stored in the database; only paths and
metadata are persisted.

## Relationships

```text
Agent 1 ─── * VideoSource ─── * Transcript
  │                │
  │                ├── * VideoAnalysis
  │                └── * Clip ─── 1 ClipMetadata
  │
  ├── 1 AgentConfig
  └── * Workflow ─── * WorkflowTask
```

Foreign keys use restrictive ownership semantics appropriate for a local
application: deleting an agent detaches optional references, while deleting a
source, workflow, or clip cascades its dependent metadata.

## Indexes and constraints

- Agent, workflow, task, clip, and model status indexes support queue/status views.
- Video URL and content hash uniqueness prevent duplicate source records.
- Foreign-key indexes support relationship lookups.
- Agent and clip metadata are one-to-one through unique foreign keys.

## Migration and seed commands

```powershell
uv run --project backend alembic upgrade head
uv run --project backend alembic downgrade base
```

`seed_defaults()` inserts only the safe `disabled/local` model registry entry
and is idempotent. It never stores secrets, API keys, passwords, or tokens.
