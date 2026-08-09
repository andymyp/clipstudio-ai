# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 010
## AI Clip Scoring Engine Implementation


Version:

1.0.0


---

# ROLE

You are implementing the intelligence ranking system of ClipStudio AI.

Act as:

```
Machine Learning Engineer

+

Recommendation System Engineer

+

AI Product Engineer
```

---

# OBJECTIVE

Build an AI-powered scoring engine.

The engine must determine:

```
Best Content

Best Segment

Best Clip Candidate
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/011-Scoring-System.md
```

---

# CORE PRINCIPLE

Score content based on:

```
Audience Value

+

Retention Potential

+

Emotional Impact
```

---

# TASK 1

Create Scoring Module

Location:

```
services/scoring/
```

Structure:

```
scoring/

├── engine.py

├── calculator.py

├── rules.py

├── weights.py

├── ranking.py

├── predictors.py

└── schemas.py
```

---

# TASK 2

Create Scoring Engine

Responsibilities:

```
Receive Analysis

Calculate Scores

Rank Candidates

Return Recommendation
```

---

# TASK 3

Create Score Schema

Output:

```
{
overall_score,

hook_score,

emotion_score,

story_score,

quality_score,

originality_score
}
```

---

# TASK 4

Implement Hook Score

Evaluate:

```
First Seconds Impact

Curiosity

Attention Trigger
```

---

# TASK 5

Implement Emotion Score

Evaluate:

```
Emotion Strength

Audience Reaction

Memorability
```

---

# TASK 6

Implement Story Score

Evaluate:

```
Narrative Flow

Conflict

Payoff
```

---

# TASK 7

Implement Retention Score

Estimate:

```
Viewer Stay Probability

Completion Rate

Rewatch Potential
```

---

# TASK 8

Implement Originality Score

Evaluate:

```
Uniqueness

Novelty

Content Similarity
```

---

# TASK 9

Implement Quality Score

Evaluate:

```
Audio Quality

Visual Quality

Content Clarity
```

---

# TASK 10

Create Weight System

Support:

```
Category Specific Weights
```

Example:

Funny:

```
Emotion 40%

Hook 35%

Story 25%
```

---

# TASK 11

Create Dynamic Scoring Rules

Agent can configure:

```
Minimum Score

Preferred Attributes

Rejected Attributes
```

---

# TASK 12

Create Segment Ranking

Input:

```
Multiple Video Segments
```

Output:

```
Ranked Segments
```

---

# TASK 13

Create Best Segment Selector

Return:

```
Start Timestamp

End Timestamp

Reason
```

---

# TASK 14

Create AI Explanation

Generate:

```
Why Selected

Score Breakdown

Expected Performance
```

---

# TASK 15

Create Scoring Memory

Store:

```
Successful Clips

Failed Predictions

User Feedback
```

---

# TASK 16

Create Feedback Learning Interface

Support:

```
Approved Clip

Rejected Clip

Manual Rating
```

---

# TASK 17

Workflow Integration

Create task:

```
Score Content
```

Input:

```
Analysis Result
```

Output:

```
Ranked Clip Candidate
```

---

# TASK 18

Event Integration

Publish:

```
ScoringStarted

ScoreGenerated

RankingCompleted
```

---

# TASK 19

API Integration

Prepare:

```
GET /videos/{id}/score
```

---

# TASK 20

Create Tests

Test:

```
Score Calculation

Ranking

Weights

Selection

Feedback
```

---

# CODING RULES

Must:

```
Keep Scoring Explainable

Avoid Black Box Only

Support Custom Rules
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Fast Calculation

Batch Processing

Caching
```

---

# SECURITY REQUIREMENTS

Protect:

```
Scoring Rules

Agent Configuration

Model Outputs
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Video Rendering

Subtitle Generation

Final Export
```

---

# VALIDATION

Run:

```
Analyze Candidate

Generate Scores

Rank Segments

Select Winner

Store Result
```

---

# SUCCESS CRITERIA

Prompt 010 complete when:

✓ Scoring engine works

✓ Multiple factors evaluated

✓ Ranking works

✓ Agent rules supported

✓ Explanation generated

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Scoring Architecture

Formula Details

Files Created

Test Results

Next Step
```
