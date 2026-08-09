# ClipStudio AI
# Implementation Prompt

## Prompt 013
## Event Driven Architecture Implementation


Version:

1.0.0


---

# ROLE

You are implementing the communication backbone of ClipStudio AI.

Act as:

```
Distributed Systems Architect

+

Backend Infrastructure Engineer

+

Event Driven Architecture Specialist
```

---

# OBJECTIVE

Build an internal event-driven communication system.

The system must support:

```
Service Communication

Workflow Triggers

Agent Reactions

Audit Logging

Async Processing
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/027-Event-Driven-Architecture.md
```

---

# CORE PRINCIPLE

Services communicate through:

```
Events

Not Direct Dependencies
```

---

# TASK 1

Create Event Module

Location:

```
packages/events/
```

Structure:

```
events/

├── bus.py

├── publisher.py

├── subscriber.py

├── registry.py

├── schemas.py

├── handlers.py

└── types.py
```

---

# TASK 2

Create Event Bus

Responsibilities:

```
Publish Events

Subscribe Handlers

Route Messages
```

---

# TASK 3

Create Event Schema

Every event contains:

```
event_id

event_type

timestamp

source

payload

metadata
```

---

# TASK 4

Create Event Types

Implement:

```
Agent Events

Workflow Events

Video Events

Analysis Events

Rendering Events

Storage Events
```

---

# TASK 5

Create Publisher Interface

Support:

```
publish(event)

publish_async(event)
```

---

# TASK 6

Create Subscriber Interface

Support:

```
subscribe()

unsubscribe()

handle()
```

---

# TASK 7

Create Event Registry

Register:

```
Event Type

Handler

Priority
```

---

# TASK 8

Implement Async Event Processing

Support:

```
Background Handling

Multiple Consumers

Failure Isolation
```

---

# TASK 9

Create Event Retry System

Handle:

```
Failed Handler

Temporary Error

Timeout
```

---

# TASK 10

Create Dead Letter Queue Interface

Store:

```
Failed Events

Error Reason

Retry Count
```

---

# TASK 11

Create Audit Event Logger

Track:

```
Event

Source

Result

Timestamp
```

---

# TASK 12

Integrate Agent Events

Support:

```
AgentCreated

AgentStarted

AgentStopped

AgentCompleted
```

---

# TASK 13

Integrate Workflow Events

Support:

```
WorkflowStarted

TaskStarted

TaskCompleted

WorkflowFailed
```

---

# TASK 14

Integrate Video Events

Support:

```
VideoDiscovered

TranscriptReady

AnalysisReady
```

---

# TASK 15

Integrate Rendering Events

Support:

```
RenderStarted

RenderCompleted

RenderFailed
```

---

# TASK 16

Create Event Driven Workflow Trigger

Example:

```
TranscriptCompleted

↓

Trigger Analysis Task
```

---

# TASK 17

Create Event Monitoring

Expose:

```
Event Count

Failed Events

Processing Time
```

---

# TASK 18

Create API Integration

Prepare:

```
GET /events

GET /events/{id}
```

---

# TASK 19

Create Event Tests

Test:

```
Publish Event

Subscribe Handler

Async Processing

Retry

Failure Handling
```

---

# TASK 20

Create Documentation

Update:

```
docs/event-architecture.md
```

Include:

```
Event Flow

Event Types

Consumers
```

---

# CODING RULES

Must:

```
Loose Coupling

Async First

Schema Validation
```

---

# PERFORMANCE REQUIREMENTS

Support:

```
High Event Volume

Concurrent Handlers

Fast Dispatch
```

---

# SECURITY REQUIREMENTS

Protect:

```
Sensitive Payload

Internal Events

Access Control
```

---

# DO NOT IMPLEMENT

Do not implement:

```
External Message Broker

Cloud Queue

Social Integration
```

Only internal architecture.

---

# VALIDATION

Run:

```
Create Event

Publish Event

Handle Event

Retry Failure

Record Audit
```

---

# SUCCESS CRITERIA

Prompt 013 complete when:

✓ Event bus works

✓ Services communicate

✓ Async handling works

✓ Retry works

✓ Audit logging works

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Event Architecture

Event Types

Files Created

Test Results

Next Step
```
