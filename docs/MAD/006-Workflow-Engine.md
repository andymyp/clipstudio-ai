# ClipStudio AI
# Master Architecture Document

Document:
006-Workflow-Engine.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 001-Vision.md
- 002-Architecture-Principles.md
- 004-System-Architecture.md
- 005-Agent-Architecture.md

Referenced By:

- 007-Discovery Engine
- 008-Segment Downloader
- 009-Transcript Pipeline
- 010-AI Analysis
- 013-Rendering Pipeline
- 017-Scheduler
- 015-Database Design

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Workflow Engine.

The Workflow Engine is responsible for:

- orchestrating all processing stages
- managing task execution
- controlling dependencies
- handling failures
- supporting resume capability
- coordinating AI agents
- maintaining execution state

The Workflow Engine is the execution backbone of ClipStudio AI.

---

# 2. Workflow Definition

A Workflow is a collection of ordered processing tasks required to transform an input into an output.

Example:

```
Video Source

↓

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

Review
```

---

# 3. Workflow Architecture

```
                Agent

                  |

                  ▼

          Workflow Generator

                  |

                  ▼

            Workflow Instance

                  |

                  ▼

             Task Graph

                  |

        ┌─────────┼─────────┐

        ▼         ▼         ▼

     Worker    Worker    Worker

        |

        ▼

      Result Store
```

---

# 4. Workflow Principles

Workflow Engine follows:

## 4.1 Pipeline Based

Every operation is a pipeline stage.

---

## 4.2 Resumable

Any completed stage does not execute again.

---

## 4.3 Observable

Every stage produces metrics.

---

## 4.4 Fault Tolerant

Failures are isolated.

---

## 4.5 Deterministic

Same input produces same execution path.

---

# 5. Workflow Types

ClipStudio AI supports:

## Content Production Workflow

Main pipeline.

```
Discovery

↓

Clip Generation

↓

Review
```

---

## Analysis Workflow

Used for existing clips.

```
Video

↓

Analysis

↓

Metadata
```

---

## Maintenance Workflow

Background operations:

```
Cleanup

↓

Indexing

↓

Optimization
```

---

# 6. Workflow Instance

A workflow instance represents one execution.

Example:

```
Workflow ID:

wf_20260803_001


Agent:

funny-agent


Source:

youtube_video_x


Status:

RUNNING
```

---

# 7. Workflow State Machine

```
CREATED

   |

   ▼

QUEUED

   |

   ▼

RUNNING

   |

 ┌─┴─────────┐

 ▼           ▼

COMPLETED   FAILED

             |

             ▼

           RETRY

             |

             ▼

          RUNNING
```

---

# 8. Workflow Status

Supported states:

## CREATED

Workflow generated.

---

## QUEUED

Waiting execution.

---

## RUNNING

Currently processing.

---

## PAUSED

Temporarily stopped.

---

## COMPLETED

Successfully finished.

---

## FAILED

Execution failed.

---

## CANCELLED

Stopped by user.

---

# 9. Task Architecture

A workflow contains tasks.

Example:

```
Workflow

├── Discovery Task

├── Transcript Task

├── Analysis Task

├── Scoring Task

├── Download Task

├── Render Task

└── Quality Task
```

---

# 10. Task Definition

Each task contains:

```
Task

├── ID

├── Type

├── Input

├── Output

├── Dependencies

├── Retry Policy

├── Timeout

├── Worker

└── Status
```

---

# 11. Task State Machine

```
CREATED

↓

READY

↓

RUNNING

↓

SUCCESS


or


FAILED

↓

RETRY

↓

RUNNING
```

---

# 12. Workflow DAG Model

Workflows are represented as Directed Acyclic Graphs.

Example:

```
             Discovery

                 |

                 ▼

            Transcript

                 |

                 ▼

             Analysis

             /       \

            ▼         ▼

       Scoring    Vision

             \       /

              ▼

          Segment Select

                 |

                 ▼

             Download

                 |

                 ▼

             Render
```

---

# 13. Why DAG Architecture

Benefits:

- parallel execution
- clear dependencies
- easier debugging
- resumable processing
- scalable execution

---

# 14. Queue Architecture

Internal queue:

```
Rust Tokio Channel
```

---

Queue contains:

```
Task ID

Priority

Agent

Workflow

Created Time
```

---

# 15. Task Priority

Priority levels:

```
CRITICAL

HIGH

NORMAL

LOW

BACKGROUND
```

Example:

User requested render:

HIGH

Cleanup:

BACKGROUND

---

# 16. Worker Architecture

Workers execute tasks.

Example:

```
Worker Pool

├── Discovery Worker

├── AI Worker

├── Download Worker

├── Render Worker

└── Index Worker
```

---

# 17. Worker Rules

Workers must:

- be stateless
- report progress
- handle errors
- release resources

Workers must not:

- modify workflow state directly
- bypass queue
- access UI

---

# 18. Checkpoint System

Every completed task creates checkpoint.

Example:

```
Transcript Completed

Checkpoint:

transcript_v1.json
```

If later stages fail:

```
Resume From:

Analysis
```

---

# 19. Resume Architecture

Example:

Before crash:

```
Discovery ✓

Transcript ✓

Analysis ✓

Download ✗
```

After restart:

```
Load checkpoint

↓

Continue Download
```

---

# 20. Retry System

Retry policy:

```
Attempt 1

↓

Wait

↓

Attempt 2

↓

Attempt 3

↓

Mark Failed
```

---

# 21. Retry Strategy

Different errors have different behavior.

Network:

Retry.

AI Model Error:

Retry.

Invalid Input:

Do not retry.

---

# 22. Timeout Management

Every task has timeout.

Example:

```
Discovery:

5 minutes


AI Analysis:

10 minutes


Render:

30 minutes
```

---

# 23. Event System

Workflow emits events.

Examples:

```
WorkflowCreated

TaskStarted

TaskCompleted

TaskFailed

WorkflowCompleted
```

---

# 24. Event Flow

```
Task

↓

Event

↓

Event Bus

↓

Subscribers
```

Subscribers:

- UI
- Logger
- Analytics
- Notification

---

# 25. Resource Management

Workflow Engine controls:

CPU

RAM

Disk

Workers

---

Default target:

```
AI workers:

2


Render workers:

1


Download workers:

1
```

---

# 26. Concurrency Rules

Parallel allowed:

```
Transcript

+

Metadata Processing
```

Not allowed:

```
Multiple heavy renders
```

---

# 27. Workflow Persistence

Workflow state stored in:

SQLite

Contains:

- workflow
- task
- status
- checkpoint
- error

---

# 28. Workflow Recovery

After application restart:

```
Load Active Workflows

↓

Check Task Status

↓

Resume Pending Tasks
```

---

# 29. Workflow Security

Workflow cannot:

- execute unknown binaries
- access restricted paths
- bypass permissions

---

# 30. Workflow API Concept

Internal interface:

```
createWorkflow()

startWorkflow()

pauseWorkflow()

resumeWorkflow()

cancelWorkflow()

getStatus()
```

---

# 31. Performance Optimization

Strategies:

- lazy task creation
- checkpoint reuse
- cache reuse
- parallel lightweight tasks
- memory cleanup

---

# 32. Workflow Example

Funny Moment Agent:

```
Agent Trigger

↓

Create Workflow

↓

Discover Videos

↓

Extract Transcript

↓

Analyze Humor

↓

Score Moments

↓

Select Timestamp

↓

Download Segment

↓

Render Vertical Video

↓

Generate Metadata

↓

Review Queue
```

---

# 33. Final Architecture

```
Agent

 |

 ▼

Workflow Engine

 |

 ▼

DAG Scheduler

 |

 ▼

Task Queue

 |

 ▼

Workers

 |

 ▼

Storage

 |

 ▼

User Review
```

---

# 34. Summary

Workflow Engine provides:

✓ Autonomous execution

✓ Resume capability

✓ Fault tolerance

✓ Parallel processing

✓ Resource control

✓ Agent orchestration

✓ Production reliability

The Workflow Engine is the execution foundation of ClipStudio AI.

---

End of Document