# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 015
## AI Quality Control System Implementation


Version:

1.0.0


---

# ROLE

You are implementing the automated quality assurance layer of ClipStudio AI.

Act as:

```
Video Quality Engineer

+

AI Evaluation Engineer

+

Media Pipeline Engineer
```

---

# OBJECTIVE

Build an automated quality control system.

The system must validate:

```
Video Quality

Audio Quality

Subtitle Quality

Content Quality

Technical Requirements
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/015-Quality-Control.md
```

---

# CORE PRINCIPLE

Every generated clip must pass:

```
Technical Validation

+

AI Quality Evaluation
```

before user review.

---

# TASK 1

Create Quality Module

Location:

```
services/quality_control/
```

Structure:

```
quality_control/

├── engine.py

├── validators.py

├── video.py

├── audio.py

├── subtitle.py

├── ai_review.py

├── rules.py

└── schemas.py
```

---

# TASK 2

Create Quality Control Engine

Responsibilities:

```
Receive Clip

Run Checks

Calculate Quality Score

Approve / Reject
```

---

# TASK 3

Create Quality Schema

Output:

```
{
status,

quality_score,

issues,

recommendations
}
```

---

# TASK 4

Implement Video Validation

Check:

```
File Exists

Duration

Resolution

Aspect Ratio

Codec

FPS
```

---

# TASK 5

Implement Audio Validation

Check:

```
Audio Exists

Volume Level

Noise Level

Synchronization
```

---

# TASK 6

Implement Subtitle Validation

Check:

```
Subtitle Exists

Timing Accuracy

Text Length

Readability
```

---

# TASK 7

Implement Content Validation

Check:

```
Transcript Match

Missing Context

Cut Quality
```

---

# TASK 8

Implement AI Review System

AI evaluates:

```
Hook

Engagement

Clarity

Value

Publish Readiness
```

---

# TASK 9

Create Quality Rules Engine

Support:

```
Minimum Score

Required Checks

Category Rules
```

---

# TASK 10

Create Automatic Rejection

Reject when:

```
Low Quality

Broken Video

Missing Audio

Bad Subtitle
```

---

# TASK 11

Create Improvement Suggestions

Generate:

```
Why Failed

How To Improve

Suggested Action
```

---

# TASK 12

Create Quality Score Calculation

Factors:

```
Technical Score

Content Score

AI Score

User Preference
```

---

# TASK 13

Create Human Review Integration

States:

```
PENDING_REVIEW

APPROVED

REJECTED

NEEDS_REVISION
```

---

# TASK 14

Create Feedback Learning

Store:

```
User Approval

User Rejection

Reason
```

Connect with:

```
Vector Memory
```

---

# TASK 15

Workflow Integration

Create task:

```
Quality Check
```

Input:

```
Rendered Clip
```

Output:

```
Quality Result
```

---

# TASK 16

Create Event Integration

Publish:

```
QualityStarted

QualityPassed

QualityFailed
```

---

# TASK 17

Create API Integration

Endpoints:

```
GET /clips/{id}/quality

POST /clips/{id}/approve

POST /clips/{id}/reject
```

---

# TASK 18

Create Quality Tests

Test:

```
Valid Video

Broken Video

Missing Subtitle

Low Quality

AI Review
```

---

# TASK 19

Create Example Rules

Examples:

```
Short Video:

Duration < 60 seconds

Vertical Ratio Required

Subtitle Required
```

---

# TASK 20

Create Documentation

Update:

```
docs/quality-control.md
```

Include:

```
Validation Flow

Rules

Approval Process
```

---

# CODING RULES

Must:

```
Separate Technical Checks

Separate AI Evaluation

Keep Rules Configurable
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Fast Validation

Parallel Checks

Low Resource Usage
```

---

# SECURITY REQUIREMENTS

Protect:

```
Quality Reports

User Feedback

Internal Scores
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Social Publishing

Automatic Posting

External Analytics
```

---

# VALIDATION

Run:

```
Render Sample Clip

Run Quality Checks

Generate Score

Approve / Reject
```

---

# SUCCESS CRITERIA

Prompt 015 complete when:

✓ Quality engine works

✓ Video validation works

✓ AI review works

✓ Approval workflow works

✓ Feedback stored

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Quality Architecture

Validation Rules

Files Created

Test Results

Next Step
```
