# Database infrastructure

SQLite is the approved local-first primary database. The runtime connection
adapter lives in `backend/app/database/session.py`; business tables and
Alembic migrations are intentionally deferred to later prompts.
