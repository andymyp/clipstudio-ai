# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 001
## Project Initialization & Application Skeleton


Version:

1.0.0


---

# ROLE

You are continuing ClipStudio AI implementation.

Act as:

```
Senior Software Architect

+

Full Stack Engineer

+

DevOps Engineer
```

---

# OBJECTIVE

Initialize the complete application skeleton.

This phase creates:

```
Backend Application

Desktop Application

Service Modules

Infrastructure

Development Environment
```

No advanced business logic yet.

---

# SOURCE OF TRUTH

Before implementation read:

```
/docs/MAD

/docs/PRD

/docs/TTD/001

/docs/TTD/002

/docs/TTD/003
```

Follow existing architecture.

---

# TASK 1

Review Prompt 000 output.

Verify:

```
Repository Structure

Configuration

Environment

Logging
```

Do not recreate existing components.

---

# TASK 2

Initialize Backend Application

Location:

```
apps/backend/
```

Create:

```
apps/backend/

├── app/

│   ├── main.py

│   ├── api/

│   ├── core/

│   ├── services/

│   ├── schemas/

│   └── dependencies/


├── tests/

├── requirements.txt

└── Dockerfile
```

---

# TASK 3

Create FastAPI Application

Requirements:

```
Async Support

OpenAPI Enabled

Health Endpoint

Configuration Loading
```

Create:

```
GET /health
```

Response:

```
{
 status:"ok"
}
```

---

# TASK 4

Create Service Architecture

Prepare:

```
services/

├── agent_service

├── workflow_service

├── discovery_service

├── analysis_service

├── rendering_service

└── storage_service
```

Each service must contain:

```
__init__.py

service.py

schemas.py
```

---

# TASK 5

Initialize Package Structure

Create:

```
packages/
```

Modules:

```
core

database

events

models
```

Purpose:

```
Reusable Internal Libraries
```

---

# TASK 6

Create Desktop Application Skeleton

Location:

```
apps/desktop/
```

Prepare:

```
src/

assets/

config/
```

Requirements:

```
Application Shell

API Client Placeholder

Navigation Structure
```

No complete UI yet.

---

# TASK 7

Create Infrastructure

Location:

```
infrastructure/
```

Create:

```
docker/

scripts/
```

---

# TASK 8

Create Local Development Stack

Prepare Docker services:

```
PostgreSQL

Qdrant

Backend
```

Create:

```
docker-compose.yml
```

---

# TASK 9

Database Connection Preparation

Create:

```
database configuration

connection manager

migration directory
```

Do not create business tables yet.

---

# TASK 10

Environment Management

Create:

```
.env.example
```

Include:

```
DATABASE_URL

QDRANT_URL

APP_ENV

LOG_LEVEL
```

Never include real secrets.

---

# TASK 11

Setup Dependency Management

Backend:

Include:

```
fastapi

uvicorn

pydantic

sqlalchemy

alembic

pytest
```

---

# TASK 12

Setup Code Quality Tools

Configure:

```
ruff

mypy

pytest

pre-commit
```

---

# TASK 13

Create Development Scripts

Location:

```
scripts/
```

Include:

```
start-dev

stop-dev

test

lint
```

---

# TASK 14

Create Initial CI Preparation

Prepare:

```
.github/workflows/
```

with:

```
test.yml
```

Tasks:

```
Install Dependencies

Run Tests

Run Lint
```

---

# TASK 15

Create Architecture Status

Update:

```
docs/implementation-status.md
```

Add:

```
Project Initialization Completed
```

---

# CODING RULES

Must:

```
Use Clean Architecture

Use Dependency Injection

Keep Services Independent
```

---

# DO NOT IMPLEMENT

Do not implement:

```
AI Models

Agent Logic

Video Processing

Rendering Pipeline

Database Entities
```

These are future phases.

---

# VALIDATION

Run:

```
Backend Startup

Docker Startup

Health Check

Test Command

Lint Command
```

---

# SUCCESS CRITERIA

Prompt 001 complete when:

✓ Backend skeleton runs

✓ Desktop skeleton exists

✓ Docker environment works

✓ Database infrastructure ready

✓ CI foundation exists

✓ Code quality tools active

---

# OUTPUT REPORT

Provide:

```
Created Files

Architecture Changes

Commands Tested

Validation Result

Next Step
```
