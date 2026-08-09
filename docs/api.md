# REST API

The deployable FastAPI application is exposed from `apps/backend/app/main.py`.
Interactive OpenAPI documentation is available at `/docs`, with the generated
schema at `/openapi.json`.

## Versioned routes

All application resources are under `/api/v1`:

- `/agents` — agent CRUD plus activate, pause, and queued-run control actions.
- `/videos` — source listing, filtering, lookup, and deletion.
- `/workflows` — workflow status, filtering, duration, errors, and cancellation.
- `/clips` — review listing, lookup, approve/reject, and queued export actions.
- `/models` — model registry listing, lookup, and activation.
- `/settings` — diagnostics-safe runtime settings read/update.
- `/system/health` — versioned health check.
- `/metrics` and `/version` — lightweight runtime diagnostics.

Successful responses use `{ "success": true, "data": ... }`. Validation,
authorization, not-found, database, and unexpected failures use the same
envelope with `success: false` and a structured `error` object.

When `CLIPSTUDIO_LOCAL_TOKEN` is configured, clients must send the matching
value in the `X-Local-Token` header. No token is persisted or logged.

The current API only manages persisted state and queues placeholder jobs;
agent intelligence, workflow execution, media processing, and rendering belong
to later implementation prompts.
