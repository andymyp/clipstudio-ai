$ErrorActionPreference = "Stop"

Write-Host "Starting ClipStudio AI backend..."
uv run --project backend uvicorn app.main:app --app-dir backend --reload
