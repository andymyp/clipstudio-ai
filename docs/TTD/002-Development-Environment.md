# ClipStudio AI
# Technical Task Document

Document:

002-Development-Environment.md


Version:

1.0.0


Status:

Approved


---

# 1. Purpose

This document defines the official development environment.

---

# 2. Development Philosophy

Environment must support:

```
Reproducibility

Automation

Isolation

Easy Setup
```

---

# 3. Target Development Machine

Primary:

```
Windows 11 Pro 64-bit
```

Hardware target:

```
AMD Ryzen 5 7430U

16GB RAM
```

---

# 4. Required Software

Install:

```
Git

Python

Node.js

Rust

FFmpeg

PostgreSQL

Qdrant
```

---

# 5. Version Requirements

## Python

Recommended:

```
Python 3.12+
```

---

## Node.js

Recommended:

```
Node.js 22 LTS
```

---

## Rust

Required for:

```
Tauri Desktop Application
```

---

## FFmpeg

Required for:

```
Video Processing

Encoding

Extraction
```

---

# 6. Package Management

Backend:

```
uv
```

or:

```
Poetry
```

---

Frontend:

```
pnpm
```

---

# 7. Python Environment

Structure:

```
backend/

├── .venv/

├── pyproject.toml

└── requirements.lock
```

---

# 8. Python Dependencies

Core:

```
FastAPI

Pydantic

SQLAlchemy

Alembic

AsyncIO
```

---

AI:

```
Transformers

PyTorch

Sentence Transformers
```

---

Media:

```
FFmpeg bindings

OpenCV
```

---

# 9. Node Environment

Desktop:

```
desktop/

├── package.json

├── pnpm-lock.yaml

└── src/
```

---

# 10. Frontend Stack

Required:

```
React

TypeScript

Vite

TailwindCSS
```

---

# 11. Desktop Runtime

Required:

```
Tauri 2.x
```

---

# 12. Database Environment

Development database:

```
PostgreSQL Local
```

---

Configuration:

```
Database Name

Username

Password

Port
```

---

# 13. Vector Database Environment

Development:

```
Qdrant Local
```

---

Mode:

```
Local Service
```

---

# 14. Environment Variables

Required file:

```
.env
```

Template:

```
.env.example
```

---

Example:

```
DATABASE_URL=

QDRANT_URL=

MODEL_PATH=

STORAGE_PATH=

LOG_LEVEL=
```

---

# 15. Configuration Rules

Never store:

```
API Keys

Passwords

Tokens
```

inside:

```
Source Code
```

---

# 16. Local Storage Setup

Create:

```
storage/

├── sources

├── segments

├── clips

├── exports

├── cache

└── temp
```

---

# 17. Development Commands

Backend:

```
start api server
```

---

Worker:

```
start worker process
```

---

Desktop:

```
start development app
```

---

# 18. VS Code Configuration

Recommended extensions:

```
Python

Pylance

ESLint

Prettier

Rust Analyzer

Docker
```

---

# 19. Integration

must read:

```
/docs/MAD

/docs/PRD

/docs/TTD
```

before implementation.

---

# 20. Git Configuration

Repository uses:

```
main

develop

feature branches
```

---

# 21. Commit Convention

Format:

```
type(scope): message
```

Example:

```
feat(agent): add agent scheduler
```

---

# 22. Development Workflow

Flow:

```
Create Branch

↓

Implement Feature

↓

Run Tests

↓

Review

↓

Merge
```

---

# 23. Code Quality Tools

Required:

Backend:

```
Ruff

Pytest

Mypy
```

Frontend:

```
ESLint

Prettier

TypeScript Check
```

---

# 24. Testing Environment

Separate:

```
Development Database

Testing Database
```

---

# 25. Failure Prevention

Environment should detect:

```
Missing Dependency

Wrong Version

Invalid Configuration
```

---

# 26. Acceptance Criteria

Development Environment is complete when:

✓ Project installs successfully

✓ Backend runs

✓ Desktop app runs

✓ Database connects

✓ AI modules load

✓ Tests execute

---

# 27. Final Definition

Development Environment provides:

```
Stable Foundation

For Building ClipStudio AI
```

---

End of Document