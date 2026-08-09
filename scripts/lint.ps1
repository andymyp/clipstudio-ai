$ErrorActionPreference = "Stop"

uv run --project backend ruff check --config backend/pyproject.toml backend tests apps/backend
uv run --project backend black --check backend tests
Push-Location backend
try {
    uv run --project pyproject.toml mypy --explicit-package-bases app
} finally {
    Pop-Location
}
