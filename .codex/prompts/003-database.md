# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 003
## Database Architecture Implementation


Version:

1.0.0


---

# ROLE

You are implementing the data foundation of ClipStudio AI.

Act as:

```
Database Architect

+

Backend Engineer

+

Data Modeling Specialist
```

---

# OBJECTIVE

Build a production-grade database system.

The database must support:

```
AI Agents

Video Discovery

Workflow Execution

AI Processing

Generated Clips

System History
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/015-Database-Implementation.md

/docs/TTD/016-Vector-Database.md
```

---

# DATABASE REQUIREMENT

Primary database:

```
PostgreSQL
```

ORM:

```
SQLAlchemy 2.x
```

Migration:

```
Alembic
```

---

# TASK 1

Create Database Structure

Location:

```
apps/backend/app/database/
```

Create:

```
database/

├── engine.py

├── session.py

├── base.py

├── migrations/

└── seed.py
```

---

# TASK 2

Configure Async Database

Requirements:

```
Async Engine

Connection Pool

Transaction Support
```

---

# TASK 3

Create Base Model

All entities must include:

```
id

created_at

updated_at
```

---

# TASK 4

Create Agent Entity

Table:

```
agents
```

Fields:

```
id

name

category

description

status

configuration

schedule

watermark

created_at

updated_at
```

---

# TASK 5

Create Agent Configuration Entity

Table:

```
agent_configs
```

Store:

```
Sources

Prompt

Model Settings

Scoring Rules
```

---

# TASK 6

Create Video Source Entity

Table:

```
video_sources
```

Store:

```
url

platform

title

duration

metadata

hash
```

---

# TASK 7

Create Transcript Entity

Table:

```
transcripts
```

Store:

```
video_id

text

segments

language

timestamps
```

---

# TASK 8

Create Analysis Entity

Table:

```
video_analysis
```

Store:

```
video_id

emotion_score

hook_score

quality_score

ai_result
```

---

# TASK 9

Create Workflow Entity

Table:

```
workflows
```

Store:

```
agent_id

status

current_step

progress

started_at

completed_at
```

---

# TASK 10

Create Workflow Task Entity

Table:

```
workflow_tasks
```

Store:

```
workflow_id

task_type

status

result

error
```

---

# TASK 11

Create Clip Entity

Table:

```
clips
```

Store:

```
source_video_id

file_path

duration

score

status

metadata
```

---

# TASK 12

Create Clip Metadata Entity

Table:

```
clip_metadata
```

Store:

```
title

description

hashtags

platform
```

---

# TASK 13

Create Model Registry Entity

Table:

```
ai_models
```

Store:

```
name

provider

type

version

status
```

---

# TASK 14

Create Processing History

Table:

```
processing_history
```

Track:

```
Actions

Events

Results
```

---

# TASK 15

Create Database Relationships

Implement:

```
Agent

↓

Workflow

↓

Task


Video

↓

Transcript

↓

Analysis

↓

Clip
```

---

# TASK 16

Create Alembic Migration

Generate:

```
Initial Schema Migration
```

---

# TASK 17

Create Repository Integration

Implement repositories:

```
AgentRepository

VideoRepository

WorkflowRepository

ClipRepository

ModelRepository
```

---

# TASK 18

Create Database Seed

Provide:

```
Default Configuration

Development Data
```

---

# TASK 19

Database Validation

Test:

```
Create Records

Query Records

Update Records

Delete Records

Relationships
```

---

# TASK 20

Create Database Documentation

Update:

```
docs/database-schema.md
```

Include:

```
Entities

Relationships

Purpose
```

---

# DATA RULES

Never:

```
Store Secrets

Store API Keys

Store Passwords
```

---

# PERFORMANCE REQUIREMENTS

Implement:

```
Indexes

Efficient Queries

Pagination Ready
```

---

# SECURITY REQUIREMENTS

Enable:

```
Safe Transactions

Input Validation

Access Control Ready
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Vector Search Logic

AI Processing

Rendering Logic
```

---

# VALIDATION

Run:

```
Database Migration

Database Connection

Repository Tests

Schema Tests
```

---

# SUCCESS CRITERIA

Prompt 003 complete when:

✓ PostgreSQL schema exists

✓ Models created

✓ Migration works

✓ Repository layer works

✓ Database tests pass

---

# OUTPUT REPORT

Provide:

```
Database Tables Created

Migration Status

Test Results

Schema Notes

Next Step
```
