# ClipStudio AI
# Master Architecture Document

Document:
012-Deduplication-Engine.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 005-Agent-Architecture.md
- 010-AI Analysis.md
- 011-Scoring Engine.md
- 016-Vector Database.md

Referenced By:

- 007-Discovery Engine
- 008-Segment Downloader
- 013-Rendering Pipeline
- 015-Database Design

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Deduplication Engine.

The Deduplication Engine prevents:

- duplicate discovery
- duplicate processing
- duplicate clips
- repeated content generation

---

# 2. Deduplication Philosophy

The system must recognize duplicates even when:

- URLs are different
- titles are different
- videos are cropped differently
- subtitles are modified
- content is re-uploaded

---

# 3. Deduplication Levels

ClipStudio AI uses multi-layer deduplication:

```
Level 1:

Source Deduplication


Level 2:

Video Deduplication


Level 3:

Segment Deduplication


Level 4:

Semantic Deduplication
```

---

# 4. Architecture Overview

```
             New Content

                 |

                 ▼

       Deduplication Engine

                 |

      ┌──────────┼──────────┐

      ▼          ▼          ▼

 Metadata     Fingerprint  Embedding


      |

      ▼

 Duplicate Decision

      |

      ▼

 Allow / Reject
```

---

# 5. Source Deduplication

Purpose:

Prevent processing the same source repeatedly.

Checks:

```
Source URL

Platform ID

Video ID
```

---

Example:

YouTube:

```
youtube.com/watch?v=abc123
```

Already exists:

Reject.

---

# 6. Metadata Fingerprinting

Creates identity from:

```
Title

Channel

Duration

Upload Date
```

Example:

Hash:

```
SHA256(metadata)
```

---

# 7. Video Fingerprinting

Used to identify identical videos.

Methods:

- file hash
- perceptual hash
- frame fingerprint

---

# 8. File Hash

Exact duplicate detection.

Algorithm:

```
SHA256
```

Example:

Same file:

```
Same hash
```

---

Limit:

Cannot detect:

- resized video
- edited video
- compressed copy

---

# 9. Perceptual Hash

Used for visual similarity.

Techniques:

```
pHash

dHash

aHash
```

---

Detects:

- resized videos
- small edits
- compression changes

---

# 10. Frame Sampling

Process:

```
Video

↓

Extract Frames

↓

Generate Hash

↓

Compare
```

---

Example:

Frames:

```
00:10

00:30

01:00
```

---

# 11. Audio Fingerprinting

Used for detecting:

- same audio
- reused clips
- reposts

---

Possible technology:

```
Chromaprint
```

---

# 12. Transcript Similarity

Transcript comparison.

Example:

Original:

```
Today I learned something interesting
```

Modified:

```
I learned something very interesting today
```

Still detected.

---

Technology:

```
Embedding Similarity
```

---

# 13. Semantic Deduplication

The most advanced layer.

Detects:

Different words but same meaning.

Example:

Video A:

```
How AI changed programming
```

Video B:

```
The future of coding with artificial intelligence
```

Meaning:

Similar.

---

# 14. Vector Database Integration

Uses:

```
LanceDB
```

Stores:

- transcript embeddings
- clip embeddings
- metadata embeddings

---

# 15. Similarity Calculation

Example:

```
Similarity:

0.95

=
Duplicate
```

---

Threshold:

```
>=0.90

Strong duplicate
```

```
0.75-0.90

Review
```

```
<0.75

Unique
```

---

# 16. Clip Fingerprint

Every generated clip receives:

```
Clip Fingerprint
```

Contains:

```
Video source

Timestamp range

Visual hash

Audio hash

Transcript embedding
```

---

# 17. Cross-Agent Deduplication

Important:

Different agents can find the same moment.

Example:

```
Funny Agent

+

Reaction Agent
```

Both find:

Same timestamp.

System:

Generate once.

---

# 18. Duplicate Decision Flow

```
New Candidate

↓

Check Source

↓

Check Metadata

↓

Check Fingerprint

↓

Check Embedding

↓

Decision
```

---

# 19. Duplicate Actions

If duplicate:

```
Reject
```

or:

```
Merge Metadata
```

---

Example:

Same clip found by:

Funny Agent

and

Entertainment Agent

Result:

One clip.

Multiple tags.

---

# 20. Deduplication Database

SQLite stores:

```
fingerprint_id

source_id

hash

embedding_id

created_date
```

---

# 21. Vector Storage

LanceDB stores:

```
embedding

metadata

reference_id
```

---

# 22. Processing Optimization

Before expensive operations:

Run cheap checks first.

Order:

```
URL Check

↓

Metadata Check

↓

Hash Check

↓

Embedding Check
```

---

# 23. Memory Optimization

Do not load:

- full videos
- all embeddings

Use:

- indexed search
- lazy loading

---

# 24. Deduplication Workflow

Example:

```
Discovery Found Video

↓

Check Existing

↓

New?

   |

  Yes

   |

Analyze


Generate Clip

↓

Create Fingerprint

↓

Store
```

---

# 25. Failure Handling

Embedding service failure:

Continue with basic checks.

---

Fingerprint failure:

Mark pending.

---

Database unavailable:

Pause processing.

---

# 26. Security

Protect:

- fingerprint database
- user history
- source information

---

# 27. Future Improvements

Possible:

- AI similarity judge
- creator relationship graph
- trend clustering
- content genealogy tracking

---

# 28. Final Architecture

```
              New Content

                  |

                  ▼

        Deduplication Engine

                  |

      ┌───────────┼───────────┐

      ▼           ▼           ▼

  Metadata    Fingerprint  Vector


                  |

                  ▼

          Duplicate Decision
```

---

# 29. Summary

Deduplication Engine provides:

✓ No repeated clips

✓ Cross-agent protection

✓ Semantic duplicate detection

✓ Storage efficiency

✓ Processing efficiency

✓ Better content diversity

This component ensures ClipStudio AI continuously produces fresh content.

---

End of Document