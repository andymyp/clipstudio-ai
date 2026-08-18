# ClipStudio AI
# Master Architecture Document

Document:
004-System-Architecture.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 001-Vision.md
- 002-Architecture-Principles.md
- 003-Tech-Stack.md

Referenced By:

- 005-Agent Architecture
- 006-Workflow Engine
- 014-Storage Architecture
- 015-Database Design
- 023-Deployment

---

# 1. Purpose

This document defines the complete system architecture of ClipStudio AI.

It describes:

- major system components
- runtime boundaries
- communication patterns
- data flow
- execution lifecycle
- subsystem responsibilities

The goal is to create a modular Local-First AI Operating System capable of automated short-form video production.

---

# 2. Architecture Overview

ClipStudio AI follows a hybrid architecture:

```
Desktop Application

+

Native Core Engine

+

AI Processing Services

+

Local Data Layer
```

High-level structure:

```
┌──────────────────────────────────────┐
│          ClipStudio AI App            │
│                                      │
│  React + TypeScript + Tauri UI       │
└──────────────────┬───────────────────┘
                   │
                   │ IPC
                   │
┌──────────────────▼───────────────────┐
│          Rust Core Engine             │
│                                      │
│ Agent Manager                         │
│ Workflow Engine                       │
│ Scheduler                             │
│ Queue                                 │
│ Resource Manager                      │
└───────────────┬──────────────────────┘
                │
                │ API / IPC
                │
┌───────────────▼──────────────────────┐
│          AI Service Layer             │
│                                      │
│ FastAPI + Python                     │
│                                      │
│ Whisper                              │
│ LLM                                  │
│ Vision                               │
│ Embedding                            │
└───────────────┬──────────────────────┘
                │
                │
┌───────────────▼──────────────────────┐
│          Local Data Layer             │
│                                      │
│ SQLite                               │
│ DuckDB                               │
│ LanceDB                              │
│ Workspace Files                      │
└──────────────────────────────────────┘
```

---

# 3. Architectural Layers

ClipStudio AI consists of five primary layers.

---

# Layer 1

## Presentation Layer

Technology:

```
React 19
+
TypeScript
+
Tauri
```

Responsibilities:

- user interaction
- dashboard
- agent configuration
- workflow monitoring
- clip review
- settings

Does NOT:

- process video
- execute AI
- access database directly

---

# Layer 2

## Application Core Layer

Technology:

```
Rust
+
Tokio
```

This is the brain of the application.

Responsibilities:

- orchestration
- lifecycle management
- scheduling
- task execution
- IPC
- resource control

---

# Layer 3

## AI Processing Layer

Technology:

```
Python
+
FastAPI
```

Responsibilities:

- AI inference
- transcript processing
- semantic analysis
- scoring
- generation

---

# Layer 4

## Data Layer

Contains:

SQLite

DuckDB

LanceDB

Filesystem

Responsibilities:

- persistence
- cache
- indexing
- analytics

---

# Layer 5

## External Integration Layer

Handles:

- video platforms
- AI providers
- external APIs

Examples:

- YouTube
- Vimeo
- future sources

---

# 4. Runtime Architecture

At runtime:

```
Application Start

↓

Tauri launches

↓

Rust Core initializes

↓

Database connection

↓

Scheduler starts

↓

AI services checked

↓

Agents loaded

↓

System Ready
```

---

# 5. Component Architecture

## Main Components

```
ClipStudio AI

├── Desktop UI
│
├── Core Engine
│
├── Agent Manager
│
├── Workflow Engine
│
├── Scheduler
│
├── Task Queue
│
├── Discovery Engine
│
├── Transcript Engine
│
├── Analysis Engine
│
├── Scoring Engine
│
├── Segment Downloader
│
├── Rendering Engine
│
├── Quality Engine
│
└── Storage Layer
```

---

# 6. Desktop UI Architecture

Frontend communicates only with Rust.

Flow:

```
React

↓

Tauri Command

↓

Rust Handler

↓

Core Service
```

The frontend never communicates directly with:

- SQLite
- Python
- FFmpeg
- filesystem workers

---

# 7. Rust Core Responsibilities

Rust acts as system coordinator.

Responsibilities:

## Application Lifecycle

Controls:

- startup
- shutdown
- recovery

---

## Agent Management

Controls:

- create agents
- activate agents
- deactivate agents

---

## Workflow Execution

Controls:

- pipeline execution
- dependencies
- retries

---

## Queue Management

Controls:

- task priority
- concurrency
- scheduling

---

## Resource Management

Controls:

- CPU usage
- RAM usage
- worker limits

---

# 8. Python AI Service Architecture

Python services are isolated from the core.

Communication:

```
Rust

↓

HTTP API / IPC

↓

FastAPI

↓

AI Worker
```

---

Python services:

```
AI Service

├── Transcript Worker
│
├── LLM Worker
│
├── Vision Worker
│
├── Embedding Worker
│
└── Classification Worker
```

---

# 9. Workflow Execution Model

Every task follows:

```
Task Created

↓

Queued

↓

Running

↓

Completed

↓

Stored

↓

Event Published
```

Failure:

```
Running

↓

Failed

↓

Retry

↓

Completed
```

---

# 10. End-to-End Data Flow

Example:

User creates agent:

```
User

↓

Agent Configuration

↓

Agent Manager

↓

Scheduler

↓

Discovery Engine

↓

Video Metadata

↓

Transcript Engine

↓

AI Analysis

↓

Scoring Engine

↓

Segment Downloader

↓

Renderer

↓

Quality Check

↓

Review Queue
```

---

# 11. Video Processing Architecture

Important rule:

Full videos are NOT downloaded.

Architecture:

```
Video Source

↓

Metadata Extraction

↓

Transcript

↓

AI Understanding

↓

Timestamp Decision

↓

Segment Download

↓

Processing
```

---

# 12. Communication Architecture

## UI ↔ Rust

Protocol:

Tauri IPC

---

## Rust ↔ Python

Protocol:

Local HTTP API

Future:

gRPC

---

## Rust ↔ Database

Direct connection.

---

## Workers ↔ Queue

Internal message passing.

---

# 13. Process Isolation

Heavy workloads are isolated.

Separate processes:

```
Main Application

|

├── AI Worker

├── FFmpeg Worker

├── Downloader Worker

└── Indexing Worker
```

Benefits:

- crash isolation
- memory cleanup
- better stability

---

# 14. Folder Architecture

Recommended:

```
ClipStudioAI

├── apps
│
│   └── desktop
│
├── core
│
│   └── rust-engine
│
├── services
│
│   └── ai-service
│
├── packages
│
├── models
│
├── workspace
│
│   ├── downloads
│   ├── clips
│   ├── renders
│   ├── cache
│   └── logs
│
└── docs
```

---

# 15. Runtime Data Ownership

Component ownership:

| Component | Owns |
|-|-|
| UI | Temporary UI state |
| Rust Core | Runtime state |
| SQLite | Application state |
| LanceDB | Embeddings |
| DuckDB | Analytics |
| Workspace | Media files |
| AI Workers | Temporary computation |

---

# 16. Failure Isolation Strategy

Failure examples:

## AI Model Failure

Result:

Only AI task fails.

Application continues.

---

## FFmpeg Failure

Result:

Render task fails.

Previous pipeline stages remain.

---

## Network Failure

Result:

Discovery pauses.

Local tasks continue.

---

# 17. Scalability Model

Current:

```
Single Laptop

Single User

Local Processing
```

Future:

```
Desktop

+

Cloud Workers

+

Distributed Rendering

+

Remote Agents
```

The architecture remains compatible.

---

# 18. Security Boundary

Trusted:

```
Core Engine

Database

Workspace
```

Restricted:

```
External Sources

Plugins

Cloud Providers
```

---

# 19. Performance Strategy

Target hardware optimization:

- limited workers
- streaming processing
- lazy loading models
- cache reuse
- incremental rendering
- background execution

---

# 20. Architecture Summary

ClipStudio AI is composed of:

```
Tauri UI

↓

Rust Core

↓

Workflow Engine

↓

AI Services

↓

Storage Layer

↓

External Sources
```

The architecture provides:

✓ Local-first operation

✓ AI-native workflow

✓ Modular components

✓ Replaceable technology

✓ Resource efficiency

✓ Future scalability

✓ Human controlled publishing

---

End of Document