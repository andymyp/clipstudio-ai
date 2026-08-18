# ClipStudio AI
# Master Architecture Document

Document:
014-Storage-Architecture.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 003-Tech-Stack.md
- 004-System-Architecture.md
- 008-Segment Downloader.md
- 013-Rendering Pipeline.md

Referenced By:

- 015-Database Design
- 016-Vector Database
- 020-Logging & Monitoring
- 023-Deployment

---

# 1. Purpose

This document defines the storage architecture of ClipStudio AI.

The Storage Architecture manages:

- application data
- video segments
- rendered clips
- AI models
- cache
- logs
- temporary files

---

# 2. Storage Philosophy

ClipStudio AI follows:

```
Store What Is Needed

Delete What Is Temporary

Reuse What Already Exists
```

---

# 3. Storage Categories

The system separates storage into:

```
1. Application Data

2. Media Workspace

3. AI Models

4. Cache

5. Logs

6. Temporary Files
```

---

# 4. Storage Architecture Overview

```
              ClipStudio AI

                    |

        ┌───────────┼───────────┐

        ▼           ▼           ▼

   Database     Workspace    Models


        |

        ▼

      Cache

        |

        ▼

      Logs
```

---

# 5. Root Workspace

Default:

```
ClipStudioAI/
```

Structure:

```
ClipStudioAI

├── app

├── database

├── workspace

├── models

├── cache

├── logs

└── config
```

---

# 6. Workspace Structure

```
workspace/

├── sources/

├── segments/

├── clips/

├── renders/

├── previews/

└── exports/
```

---

# 7. Sources Directory

Purpose:

Store temporary source information.

Contains:

```
metadata

thumbnails

subtitles
```

NOT:

Full videos.

---

# 8. Segments Directory

Contains:

Downloaded required portions only.

Example:

```
segments/

youtube_abc123/

segment_120_180.mp4
```

---

Lifecycle:

```
Created

↓

Processed

↓

Cached

↓

Deleted
```

---

# 9. Clips Directory

Contains processed intermediate clips.

Example:

```
clips/

clip_id.mp4
```

Used before final rendering.

---

# 10. Render Directory

Contains final outputs.

Structure:

```
renders/

├── review/

├── approved/

└── archived/
```

---

# 11. Preview Directory

Contains lightweight previews.

Purpose:

Fast user review.

Example:

```
preview_720p.mp4
```

---

# 12. Export Directory

Contains manually exported files.

Example:

```
TikTok

YouTube Shorts

Instagram Reels
```

---

# 13. Database Storage

Primary:

```
SQLite
```

Location:

```
database/

clipstudio.db
```

Stores:

- agents
- workflows
- tasks
- metadata
- history

---

# 14. Vector Storage

Technology:

```
LanceDB
```

Location:

```
database/vector/
```

Stores:

- embeddings
- similarity index

---

# 15. Analytics Storage

Technology:

```
DuckDB
```

Location:

```
database/analytics/
```

Stores:

- statistics
- performance metrics

---

# 16. AI Model Storage

Structure:

```
models/

├── whisper/

├── llm/

├── vision/

└── embedding/
```

---

# 17. Model Management

Models are:

- downloaded once
- versioned
- reused

---

Example:

```
models/

qwen3-8b/

v1/
```

---

# 18. Cache Architecture

Cache stores reusable data.

Example:

```
cache/

├── metadata/

├── transcripts/

├── segments/

├── embeddings/

└── renders/
```

---

# 19. Cache Rules

Cache can be deleted.

Database must remain valid.

---

Priority:

```
Database

> 

Cache

>

Temporary Files
```

---

# 20. Temporary Storage

Location:

```
temp/
```

Used for:

- FFmpeg processing
- intermediate files
- downloads

---

Rules:

Automatic cleanup.

---

# 21. File Naming Convention

Format:

```
{type}_{id}_{timestamp}_{version}
```

Example:

```
segment_abc123_120_180_v1.mp4
```

---

# 22. Storage Lifecycle

Every asset follows:

```
Created

↓

Used

↓

Cached

↓

Archived

↓

Deleted
```

---

# 23. Automatic Cleanup

Cleanup tasks:

Daily:

```
Remove temporary files
```

Weekly:

```
Remove unused cache
```

---

# 24. Storage Limits

User configurable.

Example:

```
Maximum Cache:

20GB
```

---

When exceeded:

```
Delete oldest unused files
```

---

# 25. Disk Monitoring

Monitor:

```
Available Space

Cache Size

Workspace Size
```

---

Warning levels:

```
70%

Warning


90%

Critical
```

---

# 26. Backup Strategy

Important data:

Backup:

```
Database

Configuration

Agent Definitions
```

---

Optional:

```
Rendered Clips
```

---

Do not backup:

```
Temporary Cache
```

---

# 27. Migration Strategy

Storage versions:

Example:

```
storage_v1

storage_v2
```

Migration scripts required.

---

# 28. Performance Optimization

For laptop:

Rules:

- avoid duplicate files
- stream processing
- cleanup automatically
- use SSD efficiently
- limit cache size

---

# 29. Storage Security

Protect:

- database
- API keys
- user configuration

---

Sensitive files:

Encrypted.

---

# 30. Storage Recovery

After crash:

```
Scan Workspace

↓

Validate Files

↓

Repair Database References
```

---

# 31. Example Storage Flow

```
Discovery

↓

Metadata Stored

↓

Transcript Cached

↓

AI Analysis

↓

Segment Download

↓

Render

↓

Review

↓

Archive/Delete
```

---

# 32. Final Architecture

```
                  Application

                       |

        ┌──────────────┼──────────────┐

        ▼              ▼              ▼

    Database      Workspace       Models


        |

        ▼

      Cache

        |

        ▼

      Logs
```

---

# 33. Summary

Storage Architecture provides:

✓ Efficient disk usage

✓ No unnecessary full videos

✓ Clear lifecycle management

✓ Cache optimization

✓ Recovery capability

✓ Laptop-friendly operation

The Storage Architecture ensures ClipStudio AI remains practical for local-first usage.

---

End of Document