# ClipStudio AI
# Technical Task Document

Document:

001-Repository-Structure.md


Version:

1.0.0


Status:

Approved


---

# 1. Purpose

This document defines the official repository structure.

---

# 2. Repository Philosophy

Repository follows:

```
Modular Architecture

Clear Boundaries

Independent Components
```

---

# 3. Root Repository

Final structure:

```
clipstudio-ai/

│
├── apps/
│
├── backend/
│
├── ai/
│
├── workers/
│
├── media/
│
├── database/
│
├── desktop/
│
├── models/
│
├── storage/
│
├── tests/
│
├── scripts/
│
├── docs/
│
├── config/
│
├── docker/
│
├── .env.example
│
├── README.md
│
└── LICENSE
```

---

# 4. Apps Directory

Purpose:

Application entry points.

Structure:

```
apps/

├── api/

├── worker/

└── desktop/
```

---

# 5. Backend Directory

Purpose:

Core application backend.

Structure:

```
backend/

├── api/

├── core/

├── services/

├── repositories/

├── schemas/

├── database/

└── main.py
```

---

# 6. Backend Responsibilities

Backend handles:

```
Business Logic

API

Database Access

Workflow Control

Configuration
```

---

# 7. AI Directory

Purpose:

Artificial intelligence modules.

Structure:

```
ai/

├── llm/

├── embeddings/

├── speech/

├── vision/

├── prompts/

└── evaluation/
```

---

# 8. AI Module Responsibilities

Contains:

```
Model Interface

Prompt System

AI Processing Logic
```

---

# 9. Workers Directory

Purpose:

Background processing.

Structure:

```
workers/

├── discovery/

├── analysis/

├── downloader/

├── renderer/

└── scheduler/
```

---

# 10. Worker Responsibilities

Workers execute:

```
Long Running Tasks

Queue Jobs

Media Processing
```

---

# 11. Media Directory

Purpose:

Video processing layer.

Structure:

```
media/

├── downloader/

├── processor/

├── subtitle/

├── watermark/

└── encoder/
```

---

# 12. Database Directory

Purpose:

Database management.

Structure:

```
database/

├── migrations/

├── schemas/

├── seeds/

└── backups/
```

---

# 13. Desktop Directory

Purpose:

User interface.

Structure:

```
desktop/

├── src/

├── components/

├── pages/

├── hooks/

├── services/

└── package.json
```

---

# 14. Models Directory

Purpose:

AI model storage.

Structure:

```
models/

├── llm/

├── embeddings/

├── speech/

└── vision/
```

---

# 15. Storage Directory

Purpose:

Runtime generated data.

Structure:

```
storage/

├── sources/

├── segments/

├── clips/

├── exports/

├── cache/

└── temp/
```

---

# 16. Tests Directory

Structure:

```
tests/

├── unit/

├── integration/

├── workflow/

├── performance/

└── security/
```

---

# 17. Scripts Directory

Contains:

```
Installation Scripts

Migration Scripts

Development Tools
```

---

# 18. Documentation Directory

Structure:

```
docs/

├── MAD/

├── PRD/

├── TTD/

├── ADR/

└── guides/
```

---

# 19. Configuration Directory

Contains:

```
Application Config

Model Config

Agent Config

Environment Templates
```

---

# 20. Naming Convention

Files:

```
snake_case
```

Python:

```
snake_case
```

Classes:

```
PascalCase
```

React Components:

```
PascalCase
```

---

# 21. Module Boundary Rules

Modules communicate through:

```
Interfaces

APIs

Events
```

Avoid:

```
Direct Internal Access
```

---

# 22. Dependency Rules

Allowed:

```
Backend → Database

Backend → AI

Worker → Services
```

Not allowed:

```
Database → UI

AI → Desktop
```

---

# 23. Environment Separation

Support:

```
Development

Testing

Production
```

---

# 24. Rules

Before creating files:

Must check:

```
Repository Structure

Existing Modules

Architecture Rules
```

---

# 25. Acceptance Criteria

Repository structure is complete when:

✓ All modules have clear location

✓ Components are isolated

✓ Future expansion is possible

✓ AI coding agents can navigate easily

---

# 26. Final Definition

Repository structure becomes the physical foundation of ClipStudio AI.

```
Clean Structure

+

Clear Responsibility

+

Maintainable Code
```

---

End of Document