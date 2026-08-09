# Discovery Engine

The discovery layer implements the metadata-first rule: find candidate sources
first and defer media downloads to later workflow tasks. It is asynchronous,
connector-based, and safe to run offline with deterministic static connectors.

## Architecture

```text
SearchQuery
    |
    v
DiscoveryManager -> DiscoveryEngine -> ConnectorRegistry -> SourceConnector
                          |
                          +-> normalize metadata
                          +-> rank and filter candidates
                          +-> URL/content-hash/semantic deduplication
                          +-> VideoSource + ProcessingHistory
                          +-> discovery events
```

`DiscoveryManager` is the application facade and exposes a workflow task
adapter. `DiscoveryEngine` owns the run lifecycle. Source connectors implement
`search`, `fetch_metadata`, and `validate` independently of the engine.

## Connectors

The default registry exposes deferred ports for YouTube, TikTok, Instagram,
and Reddit. They validate URL shape but perform no network requests until a
credentialed platform adapter is installed. `StaticConnector` provides an
offline/test implementation and keeps local development deterministic.

Adding a source requires implementing the `SourceConnector` protocol and
registering the connector by platform; no platform-specific branching is
added to the engine.

## Data flow

1. An agent or workflow provides keywords, category, topic, language, platform,
   and result-limit rules through `SearchQuery`.
2. Selected connectors return `VideoMetadata` records only.
3. Metadata is normalized before filtering and persistence.
4. Candidates are ranked, then filtered by duration, language, quality, or
   popularity rules.
5. URL and content-hash checks run before the optional semantic deduplicator.
6. Accepted candidates are stored as `VideoSource` records and linked to
   `ProcessingHistory`; rejected candidates retain their reason in the result.
7. The event bus publishes discovery start, found, filtered, duplicate, and
   completion events.

## Reliability and boundaries

The engine supports an async request delay and captures connector failures in
the run result. Scheduler integration is exposed through the workflow task
boundary, so recurring execution can be supplied by the existing scheduler
without coupling discovery to a platform SDK. URL validation and normalized
metadata reduce unsafe or malformed persistence input.

Transcript extraction, AI analysis, rendering, and full-video downloads are
out of scope for this phase.

## Example

```python
query, filters = funny_moments_query()
result = await manager.discover(query, filters=filters, agent_id=agent_id)
```

The example query is in
`apps/backend/app/services/discovery/templates.py`. The API already exposes
the persisted source views through `GET /api/v1/videos` and
`GET /api/v1/videos/{video_id}`; a dedicated discovery-run endpoint remains a
future application-layer addition.
