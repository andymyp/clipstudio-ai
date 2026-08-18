# ClipStudio AI
# Implementation Prompt

## Prompt 002
## Backend Core Architecture Implementation


Version:

1.0.0


---

# ROLE

You are implementing the backend foundation of ClipStudio AI.

Act as:

```
Senior Backend Engineer

+

Software Architect

+

Python Performance Engineer
```

---

# OBJECTIVE

Build a production-grade backend architecture.

The backend must become the foundation for:

```
Agent System

Workflow Engine

AI Pipeline

Rendering System

Storage System
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/004-backend-core.md

/docs/TTD/026-API-Architecture.md
```

---

# ARCHITECTURE REQUIREMENT

Use:

```
Clean Architecture

Dependency Injection

Service Layer Pattern

Repository Pattern
```

---

# TARGET STRUCTURE

Implement:

```
apps/backend/app/

├── main.py


├── api/

│   ├── router.py

│   ├── health.py

│   └── errors.py


├── core/

│   ├── config.py

│   ├── security.py

│   ├── logging.py

│   └── exceptions.py


├── services/

│   └── base.py


├── repositories/

│   └── base.py


├── database/

│   ├── session.py

│   └── base.py


├── schemas/

│   └── common.py


├── middleware/

│   ├── logging.py

│   └── error.py


└── dependencies/

    └── container.py
```

---

# TASK 1

Create Application Core

Implement:

```
Application Factory

Startup Lifecycle

Shutdown Lifecycle
```

---

# TASK 2

Create Configuration System

Support:

```
Environment Variables

YAML Configuration

Runtime Settings
```

Implement:

```
Settings Manager
```

---

# TASK 3

Create Dependency Injection

Requirements:

Services should receive:

```
Database

Configuration

Logger

External Clients
```

through injection.

---

# TASK 4

Create Database Layer

Implement:

```
Database Engine

Session Manager

Transaction Handling
```

Support:

```
Async Database Access
```

---

# TASK 5

Create Repository Pattern

Base repository:

```
Create

Read

Update

Delete

List
```

---

# TASK 6

Create Service Layer

Base service provides:

```
Business Logic Container

Transaction Handling

Validation
```

---

# TASK 7

Create API Framework

Implement:

```
Router System

API Versioning

Response Format
```

Base path:

```
/api/v1
```

---

# TASK 8

Create Standard Response Schema

All API responses:

Success:

```
{
 success:true,
 data:{}
}
```

Failure:

```
{
 success:false,
 error:{}
}
```

---

# TASK 9

Implement Error Handling

Handle:

```
Validation Error

Database Error

Application Error

Unknown Error
```

---

# TASK 10

Create Middleware

Implement:

```
Request Logging

Error Capture

Request ID
```

---

# TASK 11

Create Health System

Endpoints:

```
GET /health

GET /health/database

GET /health/system
```

---

# TASK 12

Create Background Task Foundation

Prepare:

```
Async Task Runner

Job Interface

Worker Interface
```

Do not implement workflow yet.

---

# TASK 13

Create Security Foundation

Implement:

```
Token Validation Interface

Permission Interface

Secret Handling
```

---

# TASK 14

Create API Documentation

Ensure:

```
OpenAPI Documentation

Schema Examples

Endpoint Description
```

---

# TASK 15

Create Backend Tests

Test:

```
Application Startup

Configuration

Database Connection

API Response

Error Handling
```

---

# CODE QUALITY REQUIREMENTS

Must use:

```
Python Type Hints

Async/Await

Pydantic Models

Clean Imports
```

---

# PERFORMANCE REQUIREMENTS

Backend must:

```
Start Fast

Use Async IO

Avoid Blocking Operations
```

---

# SECURITY REQUIREMENTS

Never:

```
Log Secrets

Expose Internal Errors

Hardcode Credentials
```

---

# DO NOT IMPLEMENT

Do not create:

```
Agent Logic

Workflow Logic

Video Processing

AI Models
```

---

# VALIDATION

Run:

```
Backend Server

Health Check

API Documentation

Tests

Lint
```

---

# SUCCESS CRITERIA

Prompt 002 complete when:

✓ Production backend structure exists

✓ API foundation works

✓ Database layer ready

✓ Dependency injection works

✓ Error handling works

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Implemented Components

Architecture Decisions

Test Results

Known Limitations

Next Step
```
