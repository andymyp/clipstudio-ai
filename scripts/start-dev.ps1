$ErrorActionPreference = "Stop"

Write-Host "Starting ClipStudio AI backend..."
uv run --project backend uvicorn apps.backend.app.main:app --reload
