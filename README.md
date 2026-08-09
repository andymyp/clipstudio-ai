# ClipStudio AI

ClipStudio AI is a local-first AI content production operating system. The
current implementation phase establishes the Python control-plane foundation;
pipeline features are added sequentially through the approved execution prompts.

## Development

Requirements: Python 3.12+ and `uv`.

```powershell
uv sync --project backend --group dev
uv run --project backend pytest
uv run --project backend uvicorn apps.backend.app.main:app --reload
```

The API exposes `/health`, `/api/v1/system/info`, and `/api/v1/config` during
the foundation phase. Copy `.env.example` to `.env` for local overrides.

## Architecture

The system is pipeline-based, local-first, interface-driven, and designed for
replaceable AI and infrastructure adapters. See `docs/MAD`, `docs/PRD`, and
`docs/TTD` for the governing architecture and requirements.

## Status

Prompt 000 (foundation and architecture initialization) is in progress. See
[`docs/implementation-status.md`](docs/implementation-status.md).
