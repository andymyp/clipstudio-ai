# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 007
## Video Discovery Engine Implementation


Version:

1.0.0


---

# ROLE

You are implementing the video discovery intelligence layer.

Act as:

```
Search Infrastructure Engineer

+

Data Acquisition Engineer

+

Backend Engineer
```

---

# OBJECTIVE

Build a modular video discovery system.

The system must:

```
Search Multiple Sources

Collect Metadata

Normalize Data

Detect Duplicates

Create Candidates
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/007-Discovery-Engine.md

/docs/TTD/012-Deduplication-System.md
```

---

# CORE PRINCIPLE

Discovery Engine should:

```
Find First

Download Later
```

Do not download full videos during discovery.

---

# TASK 1

Create Discovery Module

Location:

```
services/discovery/
```

Structure:

```
discovery/

├── engine.py

├── manager.py

├── sources.py

├── connectors.py

├── metadata.py

├── normalizer.py

├── filters.py

├── candidates.py

└── schemas.py
```

---

# TASK 2

Create Discovery Engine Core

Responsibilities:

```
Start Search

Collect Results

Normalize Data

Store Candidates
```

---

# TASK 3

Create Source Connector System

Architecture:

```
Discovery Engine

↓

Source Connector

↓

Platform Adapter
```

---

# TASK 4

Create Connector Interface

Every connector must implement:

```
Name

Platform

Search()

Fetch Metadata()

Validate()
```

---

# TASK 5

Prepare Multi Source Support

Support architecture for:

```
YouTube

TikTok

Instagram

Reddit

Other Sources
```

---

# TASK 6

Create Video Metadata Schema

Store:

```
Title

Description

Author

Platform

URL

Duration

Published Date

View Count

Like Count

Tags
```

---

# TASK 7

Create Search Query System

Agent provides:

```
Keywords

Category

Topic

Language
```

Discovery converts into:

```
Platform Queries
```

---

# TASK 8

Create Candidate System

Candidate states:

```
FOUND

FILTERED

QUEUED

PROCESSING

COMPLETED

REJECTED
```

---

# TASK 9

Create Metadata Normalization

Normalize:

```
Titles

Tags

Duration

Statistics

Dates
```

---

# TASK 10

Create Initial Filtering

Filter by:

```
Duration

Language

Quality

Duplicate Status
```

---

# TASK 11

Create Duplicate Detection Integration

Before queue:

Check:

```
URL Hash

Content Hash

Semantic Similarity Interface
```

---

# TASK 12

Create Discovery Storage Integration

Store:

```
Video Source

Metadata

Discovery History
```

---

# TASK 13

Create Discovery Events

Publish:

```
DiscoveryStarted

VideoFound

VideoFiltered

DiscoveryCompleted
```

---

# TASK 14

Create Workflow Integration

Discovery should support:

```
Workflow Task Execution
```

Input:

```
Agent Configuration
```

Output:

```
Video Candidates
```

---

# TASK 15

Create Scheduler Integration Interface

Support:

```
Scheduled Discovery

Recurring Search
```

---

# TASK 16

Create Rate Limit Handling

Implement:

```
Request Delay

Retry

Failure Handling
```

---

# TASK 17

Create Discovery API Integration

Endpoints:

```
GET /videos

GET /videos/{id}
```

Future:

```
POST /discovery/run
```

---

# TASK 18

Create Discovery Tests

Test:

```
Connector Loading

Metadata Parsing

Candidate Creation

Filtering

Duplicate Check
```

---

# TASK 19

Create Example Discovery Agent

Example:

```
Funny Moments Discovery
```

Configuration:

```
Keywords

Sources

Filters
```

---

# TASK 20

Create Documentation

Update:

```
docs/discovery-engine.md
```

Include:

```
Architecture

Connectors

Data Flow
```

---

# CODING RULES

Must:

```
Use Plugin Architecture

Keep Connectors Independent

Avoid Platform Coupling
```

---

# PERFORMANCE REQUIREMENTS

Discovery must:

```
Be Async

Support Multiple Sources

Avoid Full Downloads
```

---

# SECURITY REQUIREMENTS

Protect:

```
External Requests

Credentials

Rate Limits
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Transcript Extraction

AI Analysis

Video Rendering
```

---

# VALIDATION

Run:

```
Create Search Query

Execute Discovery

Generate Candidates

Store Metadata

Publish Events
```

---

# SUCCESS CRITERIA

Prompt 007 complete when:

✓ Discovery engine works

✓ Connector system exists

✓ Metadata stored

✓ Candidates created

✓ Duplicate integration ready

✓ Workflow connected

---

# OUTPUT REPORT

Provide:

```
Discovery Architecture

Sources Supported

Files Created

Tests Result

Next Step
```
