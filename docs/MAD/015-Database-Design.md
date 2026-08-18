# ClipStudio AI
# Master Architecture Document

Document:
015-Database-Design.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 003-Tech-Stack.md
- 004-System Architecture.md
- 005-Agent Architecture.md
- 006-Workflow Engine.md
- 014-Storage Architecture.md

Referenced By:

- 016-Vector Database
- 017-Scheduler
- 018-Configuration
- 020-Logging & Monitoring
- 024-Testing Strategy

---

# 1. Purpose

This document defines the database architecture of ClipStudio AI.

The database stores:

- application state
- agent configuration
- workflow state
- video metadata
- AI analysis results
- scoring results
- user feedback
- system information

---

# 2. Database Technology

Primary database:

```
SQLite
```

Reason:

- local-first
- lightweight
- zero configuration
- reliable
- sufficient for single-user application

---

# 3. Database Location

Default:

```
database/

clipstudio.db
```

---

# 4. Database Principles

Rules:

1. Database stores metadata, not large media.

2. Media files stay in workspace.

3. Every entity has unique ID.

4. All timestamps use UTC.

5. Schema changes require migration.

---

# 5. Database Overview

```
SQLite

├── Users

├── Agents

├── Agent Configurations

├── Workflows

├── Tasks

├── Videos

├── Segments

├── Transcripts

├── Analysis

├── Scores

├── Clips

├── Feedback

└── System
```

---

# 6. Entity Relationship Overview

```
Agent

 |

 ▼

Workflow

 |

 ▼

Task


Video

 |

 ▼

Transcript

 |

 ▼

Analysis

 |

 ▼

Score

 |

 ▼

Clip

 |

 ▼

Feedback
```

---

# 7. Table: agents

Purpose:

Store AI agent definitions.

Schema:

```
agents

id

name

description

category

status

created_at

updated_at
```

---

Example:

```
funny-agent

Motivation Agent
```

---

# 8. Table: agent_configs

Purpose:

Store agent behavior.

Schema:

```
agent_configs

id

agent_id

sources

objective

scoring_rules

output_rules

watermark_config

schedule_config

created_at
```

---

# 9. Table: workflows

Purpose:

Store workflow executions.

Schema:

```
workflows

id

agent_id

status

priority

started_at

completed_at

error_message
```

---

# 10. Table: workflow_tasks

Purpose:

Store individual tasks.

Schema:

```
workflow_tasks

id

workflow_id

task_type

status

progress

retry_count

started_at

completed_at
```

---

# 11. Table: videos

Purpose:

Store discovered video metadata.

Schema:

```
videos

id

source

source_id

url

title

description

channel

duration

language

thumbnail

created_at
```

---

# 12. Table: video_candidates

Purpose:

Store discovery candidates.

Schema:

```
video_candidates

id

video_id

agent_id

discovery_score

status

created_at
```

---

# 13. Table: segments

Purpose:

Store downloaded segments.

Schema:

```
segments

id

video_id

start_time

end_time

file_path

hash

size

status
```

---

# 14. Table: transcripts

Purpose:

Store transcript information.

Schema:

```
transcripts

id

video_id

language

model

confidence

status

created_at
```

---

# 15. Table: transcript_segments

Purpose:

Store timestamped transcript pieces.

Schema:

```
transcript_segments

id

transcript_id

start_time

end_time

text

confidence
```

---

# 16. Table: analyses

Purpose:

Store AI understanding results.

Schema:

```
analyses

id

video_id

model

summary

topics

emotion

created_at
```

---

# 17. Table: candidate_moments

Purpose:

Store possible clips.

Schema:

```
candidate_moments

id

analysis_id

start_time

end_time

description

confidence

status
```

---

# 18. Table: scores

Purpose:

Store scoring results.

Schema:

```
scores

id

candidate_id

hook_score

emotion_score

story_score

engagement_score

final_score

created_at
```

---

# 19. Table: clips

Purpose:

Store generated clips.

Schema:

```
clips

id

segment_id

agent_id

file_path

duration

resolution

status

created_at
```

---

# 20. Table: clip_metadata

Purpose:

Store generated posting information.

Schema:

```
clip_metadata

id

clip_id

title

description

hashtags

```

---

# 21. Table: feedback

Purpose:

Store user decisions.

Schema:

```
feedback

id

clip_id

action

comment

created_at
```

Actions:

```
approved

rejected

favorite

deleted
```

---

# 22. Table: fingerprints

Purpose:

Store duplicate detection data.

Schema:

```
fingerprints

id

content_id

type

hash

created_at
```

---

# 23. Table: settings

Purpose:

Store application settings.

Schema:

```
settings

key

value

updated_at
```

---

# 24. Index Strategy

Important indexes:

```
videos.source_id

videos.url

agents.status

workflows.status

tasks.status

scores.final_score
```

---

# 25. Database Performance

Enable:

```
WAL Mode
```

---

Configuration:

```
PRAGMA journal_mode=WAL;
```

---

Benefits:

- better concurrency
- safer writes
- faster reads

---

# 26. Data Retention

Temporary:

```
workflow logs

cache metadata
```

can expire.

Permanent:

```
agent

configuration

feedback
```

---

# 27. Migration System

Every schema change:

Example:

```
migration_001

migration_002
```

---

Migration stored:

```
database/migrations/
```

---

# 28. Backup Strategy

Backup:

```
clipstudio.db

agent configs

settings
```

---

Frequency:

User configurable.

---

# 29. Security

Protect:

- database file
- configuration
- credentials

---

Never store:

- API keys plain text

---

# 30. Query Optimization

Rules:

- paginate large lists
- use indexes
- avoid full scans
- batch inserts

---

# 31. Recovery

After corruption:

```
Restore Backup

↓

Run Integrity Check

↓

Repair References
```

---

# 32. Database Example Flow

```
Discovery

↓

videos

↓

transcripts

↓

analyses

↓

scores

↓

clips

↓

feedback
```

---

# 33. Final Architecture

```
              SQLite

                 |

 ┌───────────────┼───────────────┐

 ▼               ▼               ▼

 Agents      Workflows        Content


                 |

                 ▼

              Feedback
```

---

# 34. Summary

Database Architecture provides:

✓ Reliable application state

✓ Agent persistence

✓ Workflow tracking

✓ AI knowledge storage

✓ Feedback learning foundation

✓ Local-first operation

SQLite becomes the operational memory of ClipStudio AI.

---

End of Document