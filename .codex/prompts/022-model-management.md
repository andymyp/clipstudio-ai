# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 022
## AI Model Management System Implementation


Version:

1.0.0


---

# ROLE

You are implementing the AI model infrastructure layer of ClipStudio AI.

Act as:

```
AI Infrastructure Architect

+

ML Platform Engineer

+

Local AI Runtime Engineer
```

---

# OBJECTIVE

Build a complete AI model management system.

The system must manage:

```
LLM Models

Speech Models

Embedding Models

Vision Models

Model Versions
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD
```

---

# CORE PRINCIPLE

Models must be:

```
Replaceable

Versioned

Hardware Aware

Task Optimized
```

---

# TASK 1

Create Model Management Module

Location:

```
services/models/
```

Structure:

```
models/

├── manager.py

├── registry.py

├── downloader.py

├── router.py

├── runtime.py

├── hardware.py

├── cache.py

└── schemas.py
```

---

# TASK 2

Create Model Registry

Store:

```
Model Name

Provider

Version

Size

Requirements

Capabilities
```

---

# TASK 3

Create Model Types

Support:

```
LLM

STT

Embedding

Vision

OCR
```

---

# TASK 4

Create Model Provider Interface

Support:

```
Local Models

Remote APIs

Future Providers
```

Interface:

```
load()

unload()

generate()

health_check()
```

---

# TASK 5

Create Model Downloader

Support:

```
Download Model

Resume Download

Verify Checksum

Remove Model
```

---

# TASK 6

Create Model Storage

Structure:

```
models/

├── llm/

├── speech/

├── embedding/

├── vision/
```

---

# TASK 7

Create Hardware Detection

Detect:

```
CPU

RAM

GPU

VRAM

Disk
```

---

# TASK 8

Create Model Recommendation Engine

Based on:

```
Hardware

Task

Performance Requirement
```

Example:

```
Low VRAM

↓

Small Model
```

---

# TASK 9

Create Model Router

Route tasks:

```
Analysis

Transcript

Embedding

Vision
```

to:

```
Best Available Model
```

---

# TASK 10

Create Resource Manager

Manage:

```
GPU Memory

RAM Usage

Model Loading
```

---

# TASK 11

Create Model Cache

Support:

```
Loaded Models

Frequently Used Models

Memory Cleanup
```

---

# TASK 12

Create Model Version Control

Track:

```
Current Version

Previous Version

Compatibility
```

---

# TASK 13

Create Model Update System

Support:

```
Check Update

Download Update

Rollback
```

---

# TASK 14

Create Inference Monitoring

Track:

```
Latency

Token Usage

Memory Usage

Errors
```

---

# TASK 15

Create Model Events

Publish:

```
ModelDownloaded

ModelLoaded

ModelUpdated

ModelFailed
```

---

# TASK 16

Workflow Integration

Allow workflows to request:

```
Required Model

Task Capability
```

Example:

```
Transcript Task

↓

Speech Model
```

---

# TASK 17

Create API Integration

Prepare:

```
GET /models

GET /models/status

POST /models/download

POST /models/update
```

---

# TASK 18

Create Model Tests

Test:

```
Registry

Download

Load

Routing

Hardware Detection
```

---

# TASK 19

Create Example Configuration

Example:

```
High Performance Mode

Balanced Mode

Low Resource Mode
```

---

# TASK 20

Create Documentation

Update:

```
docs/model-management.md
```

Include:

```
Architecture

Supported Models

Hardware Guide
```

---

# CODING RULES

Must:

```
Never Hardcode Models

Separate Model Logic

Support Future AI Models
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Model Loading

VRAM Usage

Inference Speed
```

---

# SECURITY REQUIREMENTS

Protect:

```
Model Files

API Keys

Downloaded Assets
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Model Training

Fine Tuning Pipeline

AI Research Tools
```

---

# VALIDATION

Run:

```
Detect Hardware

Register Model

Download Model

Load Model

Execute Test Inference
```

---

# SUCCESS CRITERIA

Prompt 022 complete when:

✓ Model registry works

✓ Models can be downloaded

✓ Hardware detection works

✓ Routing works

✓ Resource management works

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Model Architecture

Supported Models

Hardware Compatibility

Files Created

Test Results

Next Step
```
