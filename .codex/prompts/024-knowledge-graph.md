# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 024
## Knowledge Graph Intelligence Layer Implementation


Version:

1.0.0


---

# ROLE

You are implementing the knowledge intelligence layer of ClipStudio AI.

Act as:

```
Knowledge Graph Engineer

+

AI Reasoning Architect

+

Data Intelligence Engineer
```

---

# OBJECTIVE

Build a knowledge graph system that connects:

```
Videos

Creators

Topics

Trends

Categories

Audience Patterns
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

Vector database answers:

```
"What is similar?"
```

Knowledge graph answers:

```
"What is connected?"
```

---

# TASK 1

Create Knowledge Graph Module

Location:

```
services/knowledge_graph/
```

Structure:

```
knowledge_graph/

├── graph.py

├── entities.py

├── relations.py

├── extractor.py

├── query.py

├── reasoning.py

└── schemas.py
```

---

# TASK 2

Create Graph Database Interface

Support:

```
Create Node

Create Relationship

Query Graph

Traverse Graph
```

---

# TASK 3

Prepare Graph Provider

Support:

```
Neo4j

Future Graph Databases
```

---

# TASK 4

Create Entity Types

Implement:

```
Video

Creator

Channel

Topic

Category

Trend

Audience
```

---

# TASK 5

Create Relationship Types

Implement:

```
CREATED_BY

BELONGS_TO

RELATED_TO

SIMILAR_TO

TRENDING_WITH

WATCHED_BY
```

---

# TASK 6

Create Entity Extraction Pipeline

Extract:

```
Names

Topics

Keywords

Events

Concepts
```

---

# TASK 7

Create Relationship Discovery

Detect:

```
Content Relationship

Topic Relationship

Trend Relationship
```

---

# TASK 8

Create Graph Enrichment

Combine:

```
Transcript

Metadata

AI Analysis

User Feedback
```

---

# TASK 9

Create Trend Intelligence

Track:

```
Growing Topics

Popular Patterns

Content Movement
```

---

# TASK 10

Create Creator Intelligence

Store:

```
Creator Style

Successful Content

Audience Pattern
```

---

# TASK 11

Create Content Graph Search

Support:

```
Find Related Content

Find Similar Creators

Find Emerging Topics
```

---

# TASK 12

Create Graph Reasoning Engine

Support:

```
Multi-hop Reasoning

Context Expansion

Relationship Discovery
```

---

# TASK 13

Integrate With Vector Memory

Hybrid Retrieval:

```
Vector Similarity

+

Graph Relationship
```

---

# TASK 14

Integrate With Agent System

Agents can query:

```
Knowledge Graph Context
```

Example:

```
Discovery Agent

↓

"What topics are rising?"
```

---

# TASK 15

Create Graph Events

Publish:

```
EntityCreated

RelationshipCreated

GraphUpdated
```

---

# TASK 16

Create Graph Analytics

Track:

```
Most Connected Topics

Popular Creators

Trend Evolution
```

---

# TASK 17

Create API Integration

Prepare:

```
GET /knowledge/search

GET /knowledge/entities/{id}

GET /knowledge/relationships
```

---

# TASK 18

Create Graph Tests

Test:

```
Entity Creation

Relationship Mapping

Graph Query

Reasoning
```

---

# TASK 19

Create Example Scenario

Scenario:

```
New Video Found

↓

Extract Topic

↓

Find Related Trends

↓

Compare Successful Clips

↓

Improve Scoring Decision
```

---

# TASK 20

Create Documentation

Update:

```
docs/knowledge-graph.md
```

Include:

```
Graph Model

Entities

Relationships

Query Examples
```

---

# CODING RULES

Must:

```
Keep Graph Schema Flexible

Support New Entities

Separate Extraction From Storage
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Graph Queries

Traversal Depth

Indexing
```

---

# SECURITY REQUIREMENTS

Protect:

```
Private User Data

Graph Access

Internal Intelligence
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Public Social Graph

External User Tracking

Surveillance Features
```

---

# VALIDATION

Run:

```
Create Entities

Build Relationships

Query Graph

Generate Context

Verify Agent Usage
```

---

# SUCCESS CRITERIA

Prompt 024 complete when:

✓ Graph database works

✓ Entities extracted

✓ Relationships created

✓ Hybrid AI retrieval works

✓ Agents can use graph context

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Knowledge Graph Architecture

Graph Schema

Files Created

Test Results

Next Step
```
