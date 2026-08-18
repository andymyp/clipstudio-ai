# Contributing

1. Read the relevant documents in `docs/MAD`, `docs/PRD`, and `docs/TTD`.
2. Follow the sequential prompt order in `.codex/MASTER_EXECUTION.md`.
3. Use typed, small modules with interfaces at subsystem boundaries.
4. Run tests, Ruff, Black, and mypy before opening a change.
5. Use commit messages in the form `type(scope): message`, for example
   `feat(core): add configuration loader`.

Architecture changes require an ADR and an update to the implementation report.
