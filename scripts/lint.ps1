$ErrorActionPreference = "Stop"

uv run --project backend ruff check backend tests
uv run --project backend black --check backend tests
Push-Location backend
try {
    uv run --project pyproject.toml mypy --explicit-package-bases app
} finally {
    Pop-Location
}
