# ClipStudio AI
# Implementation Prompt

## Prompt 000
## Foundation & Architecture Initialization


Version:

1.0.0


---

# ROLE

You are starting a new production-grade software project.

Act as:

```
Principal Architect

+

Lead Backend Engineer

+

AI Platform Engineer
```

---

# OBJECTIVE

Initialize the ClipStudio AI project foundation.

Do not implement business features yet.

The goal of this phase is:

```
Understand Architecture

Create Repository Foundation

Prepare Development Environment

Establish Engineering Standards
```

---

# SOURCE OF TRUTH

Before any action:

Read completely:

```
/docs/MAD

/docs/PRD

/docs/TTD
```

Required documents:

```
Architecture Documents

Product Requirements

Technical Task Documents
```

---

# IMPORTANT RULE

Do not start coding before understanding:

```
System Architecture

Data Flow

Component Responsibilities

Implementation Order
```

---

# TASK 1

Analyze existing repository.

Check:

```
Current Files

Directories

Configuration

Dependencies

Git Status
```

Report:

```
Current State

Missing Components

Required Actions
```

---

# TASK 2

Create project structure.

Required structure:

```
clipstudio-ai/

├── apps/

│   ├── desktop/

│   └── backend/


├── services/

│   ├── agents/

│   ├── workflow/

│   ├── discovery/

│   ├── analysis/

│   ├── rendering/

│   └── storage/


├── packages/

│   ├── core/

│   ├── database/

│   ├── events/

│   └── models/


├── infrastructure/

│   ├── docker/

│   └── scripts/


├── docs/


├── tests/


├── models/


├── storage/


├── logs/


└── config/
```

---

# TASK 3

Create backend foundation.

Prepare:

```
FastAPI Application

Async Runtime

Configuration Loader

Logging System
```

---

# TASK 4

Create coding standards.

Add:

```
README.md

CONTRIBUTING.md

.env.example

.gitignore
```

---

# TASK 5

Setup Python environment.

Requirements:

```
Python 3.12+

Virtual Environment

Dependency Management

Linting

Formatting
```

---

# TASK 6

Setup development dependencies.

Include:

```
pytest

ruff

mypy

black

pre-commit
```

---

# TASK 7

Create initial configuration system.

Create:

```
config/

├── app.yaml

├── database.yaml

├── models.yaml

└── storage.yaml
```

---

# TASK 8

Create base environment handling.

Support:

```
development

testing

production
```

---

# TASK 9

Create initial logging system.

Requirements:

```
Structured Logging

JSON Format

Log Levels

Log Directory
```

---

# TASK 10

Create architecture documentation.

Create:

```
docs/implementation-status.md
```

Contains:

```
Completed

In Progress

Remaining
```

---

# TASK 11

Create Git foundation.

Setup:

```
main branch

development workflow

commit convention
```

---

# CODING RULES

Always:

```
Use Type Hints

Write Clean Code

Avoid Duplication

Keep Modules Small
```

---

# DO NOT

Do not:

```
Implement Agents

Implement AI Pipeline

Implement Rendering

Implement UI
```

These belong to later prompts.

---

# VALIDATION

Before completion verify:

```
Project Structure Exists

Environment Works

Backend Starts

Configuration Loads

Logs Work
```

---

# OUTPUT REPORT

After completion provide:

```
Created Files

Changed Files

Architecture Decisions

Validation Results

Next Recommended Step
```

---

# SUCCESS CRITERIA

Prompt 000 is complete when:

✓ Repository initialized

✓ Architecture understood

✓ Backend foundation exists

✓ Configuration exists

✓ Logging exists

✓ Development environment works
