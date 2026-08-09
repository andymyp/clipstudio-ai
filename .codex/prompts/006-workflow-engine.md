# ClipStudio AI
# Implementation Prompt

## Prompt 006
## Workflow Engine Implementation


Version:

1.0.0


---

# ROLE

You are implementing the execution orchestration layer of ClipStudio AI.

Act as:

```
Workflow Engine Architect

+

Distributed Systems Engineer

+

Backend Engineer
```

---

# OBJECTIVE

Build a production-grade workflow engine.

The workflow engine must manage:

```
Task Execution

Pipeline State

Dependencies

Retries

Failures

Progress Tracking
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/006-Workflow-Engine.md

/docs/TTD/027-Event-Driven-Architecture.md
```

---

# CORE PRINCIPLE

Workflow Engine controls:

```
WHAT runs

WHEN runs

IN WHAT ORDER

WITH WHAT RESULT
```

---

# TASK 1

Create Workflow Module

Location:

```
services/workflow/
```

Structure:

```
workflow/

├── engine.py

├── manager.py

├── executor.py

├── scheduler.py

├── state.py

├── tasks.py

├── retry.py

├── events.py

└── schemas.py
```

---

# TASK 2

Create Workflow Definition System

Support:

```
Workflow Template

Workflow Instance

Workflow Task
```

---

# TASK 3

Create Workflow States

States:

```
CREATED

QUEUED

RUNNING

PAUSED

COMPLETED

FAILED

CANCELLED
```

---

# TASK 4

Create Task States

States:

```
PENDING

RUNNING

SUCCESS

FAILED

RETRYING

CANCELLED
```

---

# TASK 5

Create Workflow Engine Core

Responsibilities:

```
Load Workflow

Execute Tasks

Track State

Handle Errors

Publish Events
```

---

# TASK 6

Create Task Executor

Support:

```
Sequential Execution

Async Execution

Parallel Execution
```

---

# TASK 7

Create Task Interface

Every task must define:

```
Task Name

Input Schema

Output Schema

Execute Method

Rollback Method
```

---

# TASK 8

Create Pipeline Definition

Default Clip Pipeline:

```
Discovery

↓

Transcript

↓

Analysis

↓

Scoring

↓

Segment Download

↓

Subtitle

↓

Rendering

↓

Quality Check

↓

Storage
```

---

# TASK 9

Implement Task Dependency

Support:

```
Task A

↓

Task B

↓

Task C
```

Example:

```
Analysis requires Transcript
```

---

# TASK 10

Create Async Worker Support

Workers handle:

```
Background Jobs

Long Running Tasks

Heavy Processing
```

---

# TASK 11

Create Queue Interface

Support:

```
Job Submit

Job Consume

Job Retry

Job Cancel
```

---

# TASK 12

Create Retry System

Implement:

```
Retry Count

Retry Delay

Backoff Strategy
```

---

# TASK 13

Create Failure Handling

Handle:

```
Task Failure

Service Failure

Timeout

Resource Error
```

---

# TASK 14

Create Workflow Events

Publish:

```
WorkflowCreated

WorkflowStarted

TaskStarted

TaskCompleted

WorkflowCompleted

WorkflowFailed
```

---

# TASK 15

Create Workflow Monitoring

Expose:

```
Current Step

Progress Percentage

Execution Time

Errors
```

---

# TASK 16

Create Pause / Resume

Support:

```
Pause Workflow

Resume Workflow

Cancel Workflow
```

---

# TASK 17

Create Agent Integration

Agent should be able to:

```
Create Workflow

Start Workflow

Monitor Result
```

---

# TASK 18

Create API Integration

Connect:

```
GET /workflows

GET /workflows/{id}

POST /workflows/{id}/cancel
```

---

# TASK 19

Create Workflow Tests

Test:

```
Create Workflow

Execute Tasks

Failure Recovery

Retry

State Changes
```

---

# TASK 20

Create Example Workflow

Implement:

```
Short Video Production Workflow
```

Flow:

```
Discover

Analyze

Generate

Review
```

---

# CODING RULES

Must:

```
Use State Machine Pattern

Keep Tasks Independent

Use Event Communication
```

---

# PERFORMANCE REQUIREMENTS

Support:

```
Concurrent Jobs

Resource Limits

Cancellation
```

---

# SECURITY REQUIREMENTS

Prevent:

```
Infinite Execution

Unauthorized Jobs

Resource Exhaustion
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Discovery Algorithms

AI Analysis

Rendering Engine
```

Only create orchestration.

---

# VALIDATION

Run:

```
Create Workflow

Execute Workflow

Track Progress

Handle Failure

Retry Task
```

---

# SUCCESS CRITERIA

Prompt 006 complete when:

✓ Workflow engine works

✓ Tasks execute correctly

✓ States tracked

✓ Retry works

✓ Events published

✓ API connected

---

# OUTPUT REPORT

Provide:

```
Workflow Architecture

Created Components

Execution Tests

Performance Notes

Next Step
```
