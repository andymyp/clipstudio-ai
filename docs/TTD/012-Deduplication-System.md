# ClipStudio AI
# Technical Task Document

Document:

012-Deduplication-System.md


Version:

1.0.0


Status:

Approved


---

# 1. Purpose

This document defines Deduplication System implementation.

---

# 2. Deduplication Definition

Deduplication prevents duplicate processing and duplicate clip generation.

---

# 3. Main Objectives

System must prevent:

```
Duplicate Downloads

Duplicate Analysis

Duplicate Rendering

Duplicate Outputs
```

---

# 4. Architecture Position

```
Discovery

↓

Deduplication

↓

Analysis

↓

Scoring

↓

Rendering
```

---

# 5. Deduplication Layers

System uses multiple layers:

```
URL Detection

Metadata Detection

Content Hash

Semantic Similarity

Video Fingerprint
```

---

# 6. Layer 1: Source URL Detection

Purpose:

Detect identical sources.

---

Example:

```
same_video_url

=

duplicate
```

---

# 7. Layer 2: Metadata Similarity

Compare:

```
Title

Author

Duration

Published Date
```

---

# 8. Layer 3: File Hash

Generate:

```
SHA256 Hash
```

for:

```
Downloaded Segment
```

---

# 9. Layer 4: Perceptual Hash

Purpose:

Detect visually similar videos.

---

Compare:

```
Frames

Visual Pattern

Scene Similarity
```

---

# 10. Layer 5: Transcript Similarity

Compare:

```
Transcript Text

Meaning

Sentence Structure
```

---

# 11. Layer 6: Vector Similarity

Use:

```
Embedding Model
```

to compare:

```
Content Meaning
```

---

# 12. Deduplication Flow

```
New Candidate

↓

URL Check

↓

Metadata Check

↓

Hash Check

↓

Embedding Check

↓

Accept / Reject
```

---

# 13. Duplicate Classification

Types:

```
Exact Duplicate

Near Duplicate

Semantic Duplicate
```

---

# 14. Exact Duplicate

Example:

Same:

```
File

Hash

Timestamp
```

Action:

```
Reject
```

---

# 15. Near Duplicate

Example:

Same video:

```
Different Crop

Different Subtitle

Different Length
```

Action:

```
Review Similarity Score
```

---

# 16. Semantic Duplicate

Example:

Different source:

```
Same Speech

Same Story

Same Event
```

Action:

```
Prevent Repetition
```

---

# 17. Deduplication Database Model

Entity:

```
ContentFingerprint
```

Fields:

```
id

content_hash

embedding

source_id

created_at
```

---

# 18. Clip Memory

Store:

```
Generated Clips

Rejected Clips

Approved Clips
```

---

# 19. Agent Awareness

Duplicate checking considers:

```
Same Agent

Other Agents

Global Memory
```

---

# 20. Similarity Threshold

Example:

```
Similarity < 70%

New Content


70-90%

Review


>90%

Duplicate
```

---

# 21. Vector Database Integration

Store:

```
Transcript Embedding

Content Embedding

Clip Embedding
```

---

# 22. Performance Optimization

Order:

```
Cheap Check First

Expensive AI Check Last
```

Example:

```
URL

↓

Hash

↓

Embedding
```

---

# 23. Storage Optimization

Avoid storing:

```
Duplicate Files

Duplicate Metadata
```

---

# 24. Duplicate Event

Emit:

```
DuplicateDetected
```

---

# 25. User Control

Allow:

```
View Duplicate Reason

Override Decision

Force Process
```

---

# 26. Failure Handling

Handle:

```
Missing Hash

Embedding Error

Database Failure
```

---

# 27. Testing Requirements

Test:

```
Same Video

Edited Video

Different Source

Similar Meaning
```

---

# 28. Acceptance Criteria

Deduplication System is complete when:

✓ Detects duplicates

✓ Prevents repeated clips

✓ Supports semantic similarity

✓ Stores content memory

✓ Works across agents

---

# 29. Implementation Order

Execute:

```
1. Create Fingerprint Model

2. Add Hash Generator

3. Add Similarity Search

4. Integrate Vector Database

5. Add Duplicate Rules

6. Add Tests
```

---

# 30. Final Definition

Deduplication System becomes:

```
The Memory Layer

Of ClipStudio AI
```

preventing wasted resources and repeated content.

---

End of Document