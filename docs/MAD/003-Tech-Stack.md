# ClipStudio AI
# Master Architecture Document

Document:
003-Tech-Stack.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 001-Vision.md
- 002-Architecture-Principles.md

Referenced By:

- 004-System Architecture
- 005-Agent Architecture
- 006-Workflow Engine
- 023-Deployment
- Development Guidelines

---

# 1. Purpose

This document defines the official technology stack for ClipStudio AI.

The objective is to select technologies that provide:

- maximum performance
- minimum resource consumption
- strong AI ecosystem support
- long-term maintainability
- local-first capability
- future scalability

The technology choices are optimized for the primary target hardware:

```
OS:
Windows 11 Pro 64-bit

CPU:
AMD Ryzen 5 7430U

RAM:
16 GB

GPU:
Integrated Radeon Graphics
```

---

# 2. Technology Selection Philosophy

Technology selection follows these rules:

1.

Prefer mature technology over experimental technology.

---

2.

Prefer local execution over cloud dependency.

---

3.

Prefer lightweight architecture over distributed complexity.

---

4.

Prefer replaceable components.

---

5.

Prefer ecosystem strength.

---

6.

Avoid unnecessary infrastructure.

---

# 3. Final Technology Stack Overview

| Layer | Technology |
|---|---|
| Desktop Framework | Tauri v2 |
| Frontend | React 19 |
| Language Frontend | TypeScript |
| Build Tool | Vite |
| UI Framework | shadcn/ui |
| Styling | Tailwind CSS v4 |
| State Management | Zustand |
| Server State | TanStack Query |
| Core Engine | Rust |
| Async Runtime | Tokio |
| AI Services | Python 3.13 |
| AI API Framework | FastAPI |
| Python Package Manager | uv |
| Database | SQLite |
| Analytics Database | DuckDB |
| Vector Database | LanceDB |
| Video Processing | FFmpeg |
| Downloader | yt-dlp |
| Speech Recognition | faster-whisper |
| Scene Detection | PySceneDetect |
| OCR | PaddleOCR |
| Local LLM Runtime | Ollama |
| Embedding Model | BGE Family |
| Configuration | TOML |
| Logging | tracing |
| Testing | Rust Test + PyTest + Vitest |
| Version Control | Git |

---

# 4. Desktop Application Layer

## Technology

Tauri v2

---

## Reason

Tauri is selected instead of Electron.

Advantages:

- lower RAM usage
- smaller application size
- native OS integration
- Rust backend integration
- better performance on consumer laptops

---

## Responsibilities

Desktop layer handles:

- user interface
- agent management UI
- workflow monitoring
- configuration UI
- review interface
- clip preview

---

## Forbidden

The frontend must NOT:

- run heavy AI processing
- process video
- manage database directly
- execute external binaries directly

---

# 5. Frontend Stack

## Framework

React 19

---

## Language

TypeScript

---

## Build System

Vite

---

## UI Components

shadcn/ui

---

## Styling

Tailwind CSS v4

---

## State Management

Zustand

Used for:

- UI state
- application state
- agent state

---

## Server State

TanStack Query

Used for:

- backend communication
- async data loading
- cache management

---

# 6. Core Application Engine

## Language

Rust

---

## Runtime

Tokio

---

## Responsibilities

Rust Core controls:

- application lifecycle
- workflow execution
- agent scheduling
- task queue
- process management
- filesystem operations
- IPC communication
- resource monitoring

---

## Why Rust

Benefits:

- low memory usage
- high performance
- safe concurrency
- native desktop integration

---

# 7. AI Service Layer

## Language

Python 3.13

---

## Framework

FastAPI

---

## Responsibilities

Python handles:

- AI inference
- model communication
- ML pipeline
- embeddings
- transcript processing
- vision analysis

---

## Reason

Python remains the strongest AI ecosystem.

---

# 8. Python Dependency Management

## Tool

uv

---

## Reason

Selected over pip because:

- faster dependency resolution
- deterministic environments
- modern Python workflow

---

# 9. Database Architecture

## Primary Database

SQLite

---

## Configuration

WAL mode enabled.

---

## Responsibilities

SQLite stores:

- users
- agents
- workflows
- tasks
- clips
- metadata
- settings
- history

---

## Forbidden

The following are NOT used:

- PostgreSQL
- MySQL
- MongoDB

Reason:

The application is local-first and single-user optimized.

---

# 10. Analytics Database

## Technology

DuckDB

---

## Purpose

Used for:

- analytics
- reporting
- performance analysis
- processing statistics

---

# 11. Vector Database

## Technology

LanceDB

---

## Purpose

Stores:

- embeddings
- semantic search
- similarity matching
- duplicate detection

---

## Reason

Advantages:

- local
- lightweight
- embedded
- no server required

---

# 12. Video Processing Stack

## Core

FFmpeg

---

## Responsibilities

FFmpeg handles:

- cutting
- encoding
- subtitle rendering
- watermark
- scaling
- format conversion
- audio processing

---

## Rule

No video rendering logic should be implemented manually.

---

# 13. Video Discovery Stack

## Downloader

yt-dlp

---

## Responsibilities

Handles:

- metadata extraction
- format discovery
- subtitle extraction
- segment downloading

---

## Important Rule

Full video download is prohibited by default.

Workflow:

```
Metadata

↓

Transcript

↓

AI Analysis

↓

Timestamp Selection

↓

Segment Download
```

---

# 14. Speech Recognition

## Technology

faster-whisper

---

## Default Model

```
small
```

---

## Optional High Quality Mode

```
medium
```

---

## Reason

Optimized inference with lower resource usage.

---

# 15. Scene Understanding

## Scene Detection

PySceneDetect

---

## Vision Models

Supported:

- Florence-2
- Qwen Vision models

---

## Responsibilities

Detect:

- scene changes
- objects
- visual context

---

# 16. OCR

## Technology

PaddleOCR

---

## Purpose

Used for:

- text extraction
- subtitle verification
- visual analysis

---

# 17. Local LLM Runtime

## Technology

Ollama

---

## Primary Models

Default:

```
Qwen3 8B
```

Low memory mode:

```
Gemma 3 4B
```

---

## Used For

- title generation
- description generation
- hashtag generation
- summaries
- classification
- reasoning

---

# 18. Embedding Models

Primary:

```
BGE-small-en-v1.5
```

Alternative:

```
BGE-M3
```

---

Used for:

- semantic search
- duplicate detection
- content similarity

---

# 19. Configuration System

## Format

TOML

---

Example:

```
agents/
    funny.toml

models/
    local.toml

system.toml
```

---

Configuration must never be hardcoded.

---

# 20. Logging

## Technology

Rust:

```
tracing
tracing-subscriber
```

Python:

```
structlog
```

---

Logs must support:

- debugging
- monitoring
- audit

---

# 21. Package Management

Frontend:

```
pnpm
```

Rust:

```
cargo
```

Python:

```
uv
```

---

# 22. Testing Stack

## Rust

Built-in test framework.

---

## Python

PyTest.

---

## Frontend

Vitest.

---

## End-to-End

Playwright.

---

# 23. Development Environment

Recommended:

```
VSCode

Rust Analyzer

Python Extension

ESLint

Prettier

Claude Code

Git
```

---

# 24. Technology Not Approved

The following technologies are intentionally excluded.

---

## Electron

Reason:

High RAM consumption.

---

## Kubernetes

Reason:

Unnecessary complexity.

---

## Kafka

Reason:

Over-engineering for local desktop application.

---

## Redis

Reason:

No external queue server required.

---

## PostgreSQL

Reason:

SQLite is sufficient for target architecture.

---

## Microservices

Reason:

Desktop-first architecture does not require distributed services.

---

# 25. Future Migration Path

If ClipStudio AI grows:

Current:

```
Local Application

↓

Future:

Hybrid Local + Cloud Workers
```

Possible additions:

- cloud GPU workers
- distributed rendering
- remote agents
- enterprise accounts

The current architecture remains valid.

---

# 26. Final Technology Decision

The official ClipStudio AI technology stack is:

```
Tauri v2

+

React 19

+

TypeScript

+

Rust Core

+

Python AI Services

+

SQLite

+

DuckDB

+

LanceDB

+

FFmpeg

+

faster-whisper

+

Ollama

+

TOML Configuration
```

This stack provides the best balance between:

performance

simplicity

AI capability

local-first operation

future scalability

---

End of Document