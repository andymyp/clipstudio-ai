# Alembic migrations

Run from the repository root:

```powershell
uv run --project backend alembic upgrade head
uv run --project backend alembic downgrade base
```

The initial migration is generated from the SQLAlchemy metadata in
`apps/backend/app/database/models.py`.
