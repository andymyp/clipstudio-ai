# ClipStudio AI
# Master Architecture Document

Document:
007-Discovery-Engine.md

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
- 006-Workflow-Engine.md

Referenced By:

- 008-Segment Downloader
- 010-AI Analysis
- 012-Deduplication Engine
- 015-Database Design

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Discovery Engine.

The Discovery Engine is responsible for:

- finding potential video sources
- collecting metadata
- identifying available assets
- extracting subtitles when available
- preparing candidates for AI analysis

The Discovery Engine does NOT download complete videos.

---

# 2. Discovery Philosophy

Traditional video automation:

```
Search

↓

Download Full Video

↓

Analyze

↓

Clip
```

ClipStudio AI approach:

```
Search

↓

Metadata

↓

Transcript

↓

AI Understanding

↓

Timestamp Selection

↓

Download Segment Only
```

---

# 3. Discovery Responsibilities

The Discovery Engine handles:

✓ Source searching

✓ Metadata extraction

✓ Subtitle discovery

✓ Format discovery

✓ Source validation

✓ Candidate filtering

✓ Initial ranking

✓ Duplicate prevention

---

# 4. Discovery Non Responsibilities

Discovery does NOT:

- render videos
- generate subtitles
- perform final scoring
- download complete videos
- create final clips

---

# 5. Discovery Architecture

```
                Agent

                  |

                  ▼

          Discovery Manager

                  |

        ┌─────────┼─────────┐

        ▼         ▼         ▼

 YouTube     Vimeo     Future Sources

 Adapter     Adapter      Adapter

        |

        ▼

   Metadata Normalizer

        |

        ▼

 Candidate Database

        |

        ▼

 AI Analysis Pipeline
```

---

# 6. Source Adapter Architecture

Every source uses an adapter.

Interface:

```
IVideoSourceAdapter
```

---

Methods:

```
search()

getMetadata()

getSubtitles()

getFormats()

validate()

```

---

Example:

```
YouTubeAdapter

VimeoAdapter

LocalFileAdapter
```

---

# 7. Supported Sources

Initial:

```
YouTube

Local Files

Vimeo
```

Future:

```
TikTok

Instagram

Twitch

Facebook

X
```

---

# 8. yt-dlp Integration

Primary integration:

```
yt-dlp
```

Used for:

- metadata extraction
- subtitle extraction
- format information
- segment downloading

---

Important:

Default mode:

```
Metadata Only
```

---

Example:

```
Video URL

↓

yt-dlp metadata

↓

JSON Result
```

No media download.

---

# 9. Metadata Collection

Collected metadata:

```
Video ID

Title

Description

Channel

Duration

Upload Date

Views

Likes

Language

Categories

Tags

Thumbnail

Available subtitles

Available formats
```

---

# 10. Discovery Pipeline

```
Agent Trigger

↓

Search Query Generation

↓

Source Search

↓

Metadata Extraction

↓

Candidate Filtering

↓

Subtitle Check

↓

Database Storage

↓

AI Analysis Queue
```

---

# 11. Search Query Generation

Queries can come from:

## Agent Configuration

Example:

```
funny

reaction

unexpected moment
```

---

## AI Generated Expansion

Example:

Input:

```
funny interview
```

AI expands:

```
funny interview reaction

best interview moments

unexpected interview answer
```

---

# 12. Candidate Filtering

Before AI analysis:

Remove:

- duplicate URLs
- unsupported formats
- too short videos
- blocked sources
- unavailable content

---

Example:

Rule:

```
Minimum duration:

5 minutes
```

---

# 13. Metadata Scoring

Initial lightweight scoring:

```
Popularity

+

Duration

+

Language Match

+

Keyword Match
```

---

Example:

```
Candidate Score:

82/100
```

---

# 14. Discovery Result Model

Example:

```
VideoCandidate

{

id,

source,

url,

title,

duration,

channel,

thumbnail,

subtitleAvailable,

metadataScore

}
```

---

# 15. Subtitle Discovery

Priority:

```
1. Official subtitles

2. Auto generated subtitles

3. Whisper processing
```

---

Reason:

Avoid unnecessary video processing.

---

# 16. Discovery Storage

Metadata stored in:

SQLite

---

Stored:

- source information
- discovery history
- processing status

---

# 17. Discovery Cache

Purpose:

Avoid repeated searches.

Cache:

```
query

source

timestamp

results
```

---

# 18. Rate Limiting

Every source adapter implements:

```
request limit

delay

retry
```

---

Purpose:

Prevent:

- blocking
- excessive requests
- account restriction

---

# 19. Discovery Scheduler

Discovery is executed by:

Workflow Engine

+

Scheduler

---

Example:

```
Funny Agent

Every 6 hours

Search new videos
```

---

# 20. Discovery Events

Generated events:

```
VideoDiscovered

MetadataCollected

SubtitleFound

CandidateReady
```

---

# 21. Duplicate Prevention

Before storing candidate:

Check:

```
Source ID

URL

Hash

Embedding similarity
```

---

# 22. Error Handling

Examples:

Source unavailable:

```
Skip

Log

Continue
```

Network failure:

```
Retry
```

Invalid video:

```
Discard
```

---

# 23. Discovery Security

Rules:

- sandbox external tools
- validate URLs
- restrict filesystem access
- never execute unknown scripts

---

# 24. Performance Optimization

For Ryzen 5 7430U:

Use:

- metadata only mode
- asynchronous requests
- cached results
- limited concurrent discovery workers

Recommended:

```
Discovery Workers:

1-2
```

---

# 25. Discovery Workflow Example

Funny Moment Agent:

```
Agent

↓

Generate Queries

↓

Search YouTube

↓

Collect Metadata

↓

Find Subtitle

↓

Store Candidate

↓

Send To Analysis

```

---

# 26. Future Improvements

Possible additions:

- AI search ranking
- trending detection
- popularity prediction
- source reputation scoring
- creator tracking
- automatic topic discovery

---

# 27. Final Architecture

```
             Agent

               |

               ▼

       Discovery Engine

               |

     ┌─────────┼─────────┐

     ▼         ▼         ▼

 Sources   Metadata   Cache

     |

     ▼

 Candidate Store

     |

     ▼

 AI Analysis
```

---

# 28. Summary

Discovery Engine provides:

✓ Multi-source video discovery

✓ Metadata-first architecture

✓ No unnecessary downloads

✓ Plugin-based sources

✓ Duplicate prevention

✓ AI-ready candidates

✓ Resource-efficient operation

The Discovery Engine is the first stage of autonomous content production.

---

End of Document