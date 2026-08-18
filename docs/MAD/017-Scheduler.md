# ClipStudio AI
# Master Architecture Document

Document:
017-Scheduler.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 005-Agent Architecture.md
- 006-Workflow Engine.md
- 014-Storage Architecture.md
- 015-Database Design.md

Referenced By:

- 018-Configuration
- 020-Logging & Monitoring
- 022-Performance Optimization
- 023-Deployment

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Scheduler.

The Scheduler controls when and how AI agents execute automated workflows.

---

# 2. Scheduler Philosophy

ClipStudio AI uses:

```
Autonomous Execution

+

User Control
```

Agents can:

- run automatically
- be paused
- be disabled
- execute manually

---

# 3. Responsibilities

Scheduler handles:

✓ task timing

✓ agent activation

✓ workflow triggering

✓ queue management

✓ resource awareness

✓ retry scheduling

✓ background execution

---

# 4. Non Responsibilities

Scheduler does NOT:

- analyze videos
- download content
- score clips
- render videos

It only decides:

"When should something run?"

---

# 5. Architecture Overview

```
              User Config

                  |

                  ▼

             Scheduler Core

                  |

       ┌──────────┼──────────┐

       ▼          ▼          ▼

    Agents      Queue     Workers


                  |

                  ▼

             Workflow Engine
```

---

# 6. Scheduler Technology

Recommended:

```
APScheduler
```

Reason:

- Python native
- lightweight
- supports cron
- suitable for local app

---

# 7. Scheduling Types

Supported:

```
Interval Schedule

Cron Schedule

Manual Trigger

Event Trigger
```

---

# 8. Interval Schedule

Example:

Run every:

```
6 hours
```

Use case:

Discovery agent.

---

# 9. Cron Schedule

Example:

```
Every day

09:00

15:00

21:00
```

---

# 10. Manual Trigger

User can execute:

```
Run Now
```

without waiting scheduler.

---

# 11. Event Trigger

Examples:

```
New source detected

Previous task completed

System idle
```

---

# 12. Agent Scheduling Model

Each agent has:

```
schedule_config
```

Contains:

```
enabled

frequency

priority

max_runs

time_window
```

---

# 13. Agent States

Available states:

```
ACTIVE

PAUSED

DISABLED

ERROR

RUNNING
```

---

# 14. Scheduler Flow

```
Timer Trigger

↓

Check Agent Status

↓

Check System Resource

↓

Create Workflow

↓

Send To Queue

↓

Worker Execution
```

---

# 15. Queue System

Scheduler does not execute directly.

It creates jobs.

Flow:

```
Scheduler

↓

Task Queue

↓

Worker

↓

Workflow Engine
```

---

# 16. Task Priority

Priority levels:

```
HIGH

NORMAL

LOW
```

---

Example:

Manual user request:

HIGH

Automatic discovery:

NORMAL

Maintenance:

LOW

---

# 17. Resource-Aware Scheduling

Important for:

```
Ryzen 5 7430U

16GB RAM
```

Before running:

Check:

```
CPU Usage

Memory Usage

Disk Space
```

---

# 18. Resource Rules

Example:

If RAM:

```
>85%
```

Action:

Pause new jobs.

---

CPU:

```
>90%
```

Action:

Delay execution.

---

# 19. Worker Management

Recommended:

```
1-2 workers
```

---

Reason:

Avoid:

- RAM pressure
- CPU overload
- thermal throttling

---

# 20. Concurrent Agent Limit

Default:

```
Maximum active agents:

2
```

---

Example:

Running:

```
Funny Agent

+

Motivation Agent
```

---

# 21. Retry System

Failed task:

```
Retry

↓

Increase delay

↓

Retry again
```

---

Example:

```
Attempt 1:

5 minutes


Attempt 2:

15 minutes
```

---

# 22. Retry Limit

Default:

```
3 retries
```

After:

```
FAILED
```

---

# 23. Scheduler Database

Stored in SQLite.

Tables:

```
scheduled_jobs

job_history

execution_state
```

---

# 24. Job History

Stores:

```
job_id

agent_id

start_time

end_time

status

result
```

---

# 25. Pause / Resume

User actions:

```
Pause Agent

↓

Scheduler ignores jobs
```

Resume:

```
Enable Agent

↓

Continue Schedule
```

---

# 26. Shutdown Handling

When application closes:

```
Stop New Jobs

↓

Finish Current Task

↓

Save State
```

---

# 27. Recovery

After restart:

```
Load Pending Jobs

↓

Restore State

↓

Continue
```

---

# 28. Resource Optimization

Rules:

- avoid running multiple AI models
- schedule heavy jobs during idle time
- cleanup before large tasks
- prioritize user actions

---

# 29. Example Schedule

Funny Agent:

```
Every 4 hours
```

Workflow:

```
Discovery

↓

Transcript

↓

Analysis

↓

Score

↓

Render
```

---

# 30. Future Improvements

Possible:

- AI-based scheduling
- workload prediction
- battery-aware scheduling
- cloud worker delegation
- distributed agents

---

# 31. Final Architecture

```
              Scheduler

                  |

        ┌─────────┼─────────┐

        ▼         ▼         ▼

     Timer     Queue    Resource


                  |

                  ▼

            Workflow Engine

                  |

                  ▼

              AI Agents
```

---

# 32. Summary

Scheduler provides:

✓ Fully automatic agents

✓ User control

✓ Resource awareness

✓ Reliable execution

✓ Background automation

✓ Laptop-friendly operation

The Scheduler is the automation controller of ClipStudio AI.

---

End of Document