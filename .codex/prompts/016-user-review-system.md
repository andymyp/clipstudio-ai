# ClipStudio AI
# Implementation Prompt

## Prompt 016
## User Review System Implementation


Version:

1.0.0


---

# ROLE

You are implementing the human-in-the-loop review layer of ClipStudio AI.

Act as:

```
Product Backend Engineer

+

Workflow Designer

+

Human Feedback System Engineer
```

---

# OBJECTIVE

Build a user review system.

The system must allow users to:

```
View Generated Clips

Preview Results

Approve Clips

Reject Clips

Provide Feedback

Request Revision
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/017-Review-System.md
```

---

# CORE PRINCIPLE

AI suggests.

Human decides.

Feedback improves AI.

---

# TASK 1

Create Review Module

Location:

```
services/review/
```

Structure:

```
review/

├── manager.py

├── queue.py

├── decision.py

├── feedback.py

├── ranking.py

└── schemas.py
```

---

# TASK 2

Create Review Entity

Store:

```
Clip ID

User ID

Status

Decision

Feedback

Timestamp
```

---

# TASK 3

Create Review States

Implement:

```
WAITING_REVIEW

IN_REVIEW

APPROVED

REJECTED

REVISION_REQUESTED
```

---

# TASK 4

Create Review Queue

Responsibilities:

```
Receive Clips

Prioritize Clips

Serve User Review
```

---

# TASK 5

Create Review Ranking

Sort by:

```
AI Score

Quality Score

Priority

Created Date
```

---

# TASK 6

Create Clip Preview System

Support:

```
Video Preview

Thumbnail

Metadata

AI Explanation
```

---

# TASK 7

Create Approval Flow

When approved:

Trigger:

```
ClipApproved Event
```

Actions:

```
Update Status

Store Decision

Save Feedback
```

---

# TASK 8

Create Rejection Flow

When rejected:

Store:

```
Reason

Category

Notes
```

---

# TASK 9

Create Revision Request

Support:

```
Subtitle Fix

Different Cut

Different Segment

Quality Improvement
```

---

# TASK 10

Create Feedback Schema

Support:

```
Rating

Comment

Reason

Preference
```

---

# TASK 11

Create Learning Integration

Send feedback to:

```
Vector Memory

Agent Memory

Scoring System
```

---

# TASK 12

Create User Preference System

Learn:

```
Preferred Categories

Preferred Style

Preferred Duration

Preferred Format
```

---

# TASK 13

Create Review Events

Publish:

```
ReviewCreated

ClipApproved

ClipRejected

FeedbackSubmitted
```

---

# TASK 14

Workflow Integration

After:

```
Quality Passed
```

Automatically:

```
Create Review Task
```

---

# TASK 15

Create API Integration

Endpoints:

```
GET /review/queue

GET /review/{id}

POST /review/{id}/approve

POST /review/{id}/reject

POST /review/{id}/feedback
```

---

# TASK 16

Create Notification Interface

Prepare:

```
New Clip Ready

Review Reminder

Processing Complete
```

---

# TASK 17

Create Review History

Store:

```
Previous Decisions

Feedback Timeline

Changes
```

---

# TASK 18

Create Review Tests

Test:

```
Queue Creation

Approve

Reject

Feedback

Learning Update
```

---

# TASK 19

Create Example Review Flow

Scenario:

```
Generated Clip

↓

Quality Passed

↓

User Review

↓

Approve

↓

Ready For Publishing
```

---

# TASK 20

Create Documentation

Update:

```
docs/user-review-system.md
```

Include:

```
Review Flow

States

Feedback Loop
```

---

# CODING RULES

Must:

```
Support Human Decision

Store Feedback

Enable Continuous Improvement
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Queue Loading

Preview Generation

Multiple Users
```

---

# SECURITY REQUIREMENTS

Protect:

```
User Decisions

Private Clips

Feedback Data
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Automatic Social Publishing

External Platform Upload
```

---

# VALIDATION

Run:

```
Generate Clip

Add Review Queue

Approve Clip

Store Feedback

Verify Learning
```

---

# SUCCESS CRITERIA

Prompt 016 complete when:

✓ Review queue works

✓ Approval works

✓ Rejection works

✓ Feedback stored

✓ AI learning connected

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Review Architecture

User Flow

Files Created

Test Results

Next Step
```
