# ClipStudio AI
# Technical Task Document

Document:

011-Scoring-System.md


Version:

1.0.0


Status:

Approved


---

# 1. Purpose

This document defines Scoring Engine implementation.

---

# 2. Scoring Definition

Scoring Engine calculates quality and potential value of video segments.

---

# 3. Main Objective

Select:

```
Best Clips

Before Rendering
```

---

# 4. Architecture Position

```
AI Analysis

↓

Scoring Engine

↓

Segment Selection

↓

Rendering Pipeline
```

---

# 5. Scoring Responsibilities

Handles:

```
Quality Evaluation

Ranking

Filtering

Prioritization
```

---

# 6. Scoring Factors

Main factors:

```
Hook Score

Emotion Score

Content Score

Retention Score

Uniqueness Score

Platform Score
```

---

# 7. Hook Score

Measures:

```
First Seconds Impact
```

Evaluation:

```
Curiosity

Strong Opening

Unexpected Moment
```

---

# 8. Emotion Score

Measures:

```
Audience Emotional Response
```

Categories:

```
Funny

Surprise

Inspiration

Sadness

Excitement
```

---

# 9. Content Value Score

Measures:

```
Information

Story

Entertainment
```

---

# 10. Retention Score

Predicts:

```
Viewer Watch Completion
```

Factors:

```
Pacing

Story Flow

Length
```

---

# 11. Uniqueness Score

Measures:

```
Originality

Duplicate Probability

Novelty
```

---

# 12. Platform Score

Different platforms:

```
TikTok

YouTube Shorts

Instagram Reels
```

may use different weights.

---

# 13. Scoring Formula

Default:

```
Final Score =

Hook * 25%

+

Emotion * 25%

+

Content * 20%

+

Retention * 15%

+

Uniqueness * 15%
```

---

# 14. Agent Custom Weight

Each agent can override:

```
Score Configuration
```

Example:

Funny Agent:

```
Emotion 40%

Hook 30%
```

---

# 15. Score Range

Standard:

```
0 - 100
```

---

# 16. Quality Threshold

Example:

```
<50

Reject


50-80

Review


>80

High Priority
```

---

# 17. Score Explanation

Every score must provide:

```
Final Score

Factor Breakdown

Reason
```

---

Example:

```
Score: 87

Reason:

Strong Hook

High Emotion

Unique Moment
```

---

# 18. Scoring Database Model

Entity:

```
ClipScore
```

Fields:

```
id

clip_id

hook_score

emotion_score

final_score

explanation
```

---

# 19. Ranking System

Candidates sorted by:

```
Highest Score

↓

Lowest Score
```

---

# 20. Batch Scoring

Support:

```
Multiple Candidates
```

---

# 21. AI + Rule Hybrid

Scoring combines:

```
AI Judgment

+

Deterministic Rules
```

---

# 22. Rule Examples

Reject:

```
Too Short

No Audio

Duplicate Content
```

---

# 23. Scoring Cache

Avoid:

```
Repeated AI Evaluation
```

Store:

```
Input Hash

Model Version

Score Result
```

---

# 24. Feedback Learning

Future improvement:

Use:

```
Approved Clips

Rejected Clips
```

to improve scoring.

---

# 25. Performance Optimization

Before scoring:

Filter:

```
Invalid

Duplicate

Low Quality
```

---

# 26. Hardware Optimization

Target:

```
Ryzen 5 7430U

16GB RAM
```

Strategy:

```
Metadata Filtering First

AI Scoring Second
```

---

# 27. Failure Handling

Handle:

```
AI Failure

Invalid Score

Missing Data
```

---

# 28. Testing Requirements

Test:

```
Formula Accuracy

Weight Configuration

Ranking Result

Threshold Filtering
```

---

# 29. Acceptance Criteria

Scoring Engine is complete when:

✓ Calculates score

✓ Explains ranking

✓ Filters low quality clips

✓ Supports agent rules

✓ Improves selection quality

---

# 30. Implementation Order

Execute:

```
1. Create Score Model

2. Create Scoring Service

3. Implement Formula

4. Add AI Evaluation

5. Add Agent Weight

6. Add Tests
```

---

# 31. Final Definition

Scoring Engine becomes:

```
The Selection Intelligence

Of ClipStudio AI
```

---

End of Document