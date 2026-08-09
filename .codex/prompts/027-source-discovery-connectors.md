# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 027
## Universal Source Discovery Connectors Implementation


Version:

1.0.0


---

# ROLE

You are implementing the universal content discovery layer of ClipStudio AI.

Act as:

```
Data Acquisition Architect

+

Web Intelligence Engineer

+

AI Search Infrastructure Engineer
```

---

# OBJECTIVE

Build a modular content discovery system.

The system must discover:

```
Videos

Articles

Social Content

Trends

Media Sources
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

Discovery must be:

```
Multi Source

Replaceable

Scalable

Duplicate Free
```

---

# TASK 1

Create Discovery Connector Module

Location:

```
services/discovery/
```

Structure:

```
discovery/

├── manager.py

├── connectors/

├── normalizer.py

├── ranking.py

├── filters.py

├── cache.py

└── schemas.py
```

---

# TASK 2

Create Connector Interface

Every connector must support:

```
search()

fetch_metadata()

get_content()

health_check()
```

---

# TASK 3

Create Source Registry

Store:

```
Source Name

Connector Type

Capabilities

Status

Rate Limit
```

---

# TASK 4

Implement Video Source Connectors

Prepare:

```
YouTube

TikTok

Instagram

Reddit Video

Other Sources
```

---

# TASK 5

Implement Web Discovery Connector

Support:

```
RSS Feed

Web Pages

News Sources

Blogs
```

---

# TASK 6

Create MCP Integration Layer

Support:

```
External Tools

Search Tools

Browser Tools

Data Providers
```

---

# TASK 7

Create Content Normalization

Convert:

```
Different Sources

↓

Unified Content Schema
```

Schema:

```
Content ID

Source

URL

Title

Author

Timestamp

Metadata
```

---

# TASK 8

Create Metadata Extraction

Extract:

```
Title

Description

Tags

Author

Duration

Statistics
```

---

# TASK 9

Create Source Ranking System

Rank by:

```
Content Quality

Freshness

Popularity

Agent Preference
```

---

# TASK 10

Create Duplicate Detection

Check:

```
URL Duplicate

Hash Duplicate

Semantic Duplicate
```

Integrate:

```
Vector Memory
```

---

# TASK 11

Create Discovery Filters

Filter:

```
Language

Duration

Category

Keyword

Quality
```

---

# TASK 12

Create Trend Discovery

Detect:

```
Rising Topics

Popular Videos

Emerging Content
```

Integrate:

```
Knowledge Graph
```

---

# TASK 13

Create Discovery Cache

Store:

```
Previous Results

Source Metadata

Search History
```

---

# TASK 14

Create Rate Limit Manager

Handle:

```
API Limits

Request Delay

Connector Health
```

---

# TASK 15

Create Discovery Events

Publish:

```
ContentDiscovered

MetadataExtracted

SourceFailed
```

---

# TASK 16

Integrate Agent System

Allow:

```
Discovery Agent

↓

Select Best Sources

↓

Collect Content
```

---

# TASK 17

Integrate Scheduler

Support:

```
Scheduled Discovery Jobs
```

---

# TASK 18

Create Discovery API

Endpoints:

```
GET /sources

GET /discovery/search

GET /discovery/status
```

---

# TASK 19

Create Discovery Tests

Test:

```
Connector

Search

Metadata Extraction

Duplicate Detection

Ranking
```

---

# TASK 20

Create Documentation

Update:

```
docs/source-discovery.md
```

Include:

```
Connector Architecture

Supported Sources

Extension Guide
```

---

# CODING RULES

Must:

```
Never Couple To One Platform

Respect Source Rules

Keep Connectors Independent
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Parallel Discovery

Caching

API Usage
```

---

# SECURITY REQUIREMENTS

Protect:

```
API Credentials

Source Access

User Queries
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Copyright Bypass

Unauthorized Download

Automatic Publishing
```

---

# VALIDATION

Run:

```
Register Connector

Search Content

Normalize Result

Detect Duplicate

Send To Pipeline
```

---

# SUCCESS CRITERIA

Prompt 027 complete when:

✓ Connector system works

✓ Multiple sources supported

✓ MCP ready

✓ Ranking works

✓ Duplicate detection works

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Discovery Architecture

Connector List

Files Created

Test Results

Next Step
```
