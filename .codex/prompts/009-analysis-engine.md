# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 009
## AI Video Analysis Engine Implementation


Version:

1.0.0


---

# ROLE

You are implementing the content intelligence layer of ClipStudio AI.

Act as:

```
AI Engineer

+

LLM Application Architect

+

Machine Learning Engineer
```

---

# OBJECTIVE

Build an AI analysis engine capable of understanding video content.

The engine must analyze:

```
Meaning

Emotion

Story

Hook

Context

Engagement Potential
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/010-AI-Analysis-System.md
```

---

# CORE PRINCIPLE

The AI should understand:

```
Why A Video Segment Is Valuable
```

not only:

```
What The Video Says
```

---

# TASK 1

Create Analysis Module

Location:

```
services/analysis/
```

Structure:

```
analysis/

├── engine.py

├── analyzer.py

├── providers.py

├── prompts.py

├── context.py

├── extractors.py

├── validators.py

└── schemas.py
```

---

# TASK 2

Create Analysis Engine

Responsibilities:

```
Receive Transcript

Understand Content

Generate Insights

Store Analysis
```

---

# TASK 3

Create AI Provider Interface

Support:

```
Local LLM

Cloud LLM

Future Models
```

Interface:

```
analyze()

summarize()

classify()

health_check()
```

---

# TASK 4

Create Model Abstraction

Never hardcode:

```
Specific LLM Provider
```

Use:

```
Model Manager
```

---

# TASK 5

Create Content Understanding Pipeline

Flow:

```
Input Context

↓

Prompt Construction

↓

AI Reasoning

↓

Structured Output

↓

Validation
```

---

# TASK 6

Implement Content Classification

Detect:

```
Category

Topic

Theme

Audience
```

Examples:

```
Funny

Inspirational

Sad

Educational

Entertainment
```

---

# TASK 7

Implement Emotion Analysis

Analyze:

```
Emotion Type

Intensity

Audience Reaction
```

Examples:

```
Joy

Surprise

Sadness

Anger

Inspiration
```

---

# TASK 8

Implement Hook Detection

Detect:

```
Opening Strength

Attention Trigger

First Seconds Impact
```

---

# TASK 9

Implement Story Understanding

Analyze:

```
Beginning

Conflict

Resolution

Payoff
```

---

# TASK 10

Implement Key Moment Extraction

Identify:

```
Important Timestamp

Interesting Segment

Peak Moment
```

---

# TASK 11

Create Structured AI Output

Format:

```
{
category,

summary,

emotion,

hook,

story,

key_moments
}
```

---

# TASK 12

Create Prompt Management System

Store:

```
System Prompt

Analysis Prompt

Category Prompt

Evaluation Prompt
```

---

# TASK 13

Create Analysis Memory Integration

Store:

```
Previous Decisions

Successful Patterns

Rejected Patterns
```

---

# TASK 14

Create Workflow Integration

Support:

```
Analyze Video Task
```

Input:

```
Transcript

Metadata
```

Output:

```
Analysis Result
```

---

# TASK 15

Create Event Integration

Publish:

```
AnalysisStarted

AnalysisCompleted

AnalysisFailed
```

---

# TASK 16

Create Analysis Cache

Avoid repeated AI calls.

Use:

```
Transcript Hash

Model Version

Prompt Version
```

---

# TASK 17

Create API Integration

Prepare:

```
GET /videos/{id}/analysis
```

---

# TASK 18

Create Validation Layer

Validate:

```
AI Output Schema

Missing Fields

Invalid Values
```

---

# TASK 19

Create Analysis Tests

Test:

```
Input Transcript

AI Response

Schema Validation

Cache

Failure Handling
```

---

# TASK 20

Create Documentation

Update:

```
docs/analysis-engine.md
```

Include:

```
AI Flow

Models

Output Format
```

---

# CODING RULES

Must:

```
Use Structured Output

Separate Prompts From Code

Keep Models Replaceable
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Token Usage

Response Time

Caching
```

---

# SECURITY REQUIREMENTS

Protect:

```
User Data

Prompt Data

API Credentials
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Final Scoring Algorithm

Rendering

Subtitle Generation
```

---

# VALIDATION

Run:

```
Analyze Sample Transcript

Generate Structured Result

Validate Output

Store Analysis
```

---

# SUCCESS CRITERIA

Prompt 009 complete when:

✓ AI analysis engine works

✓ Provider abstraction exists

✓ Content understanding works

✓ Structured output generated

✓ Workflow integrated

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Analysis Architecture

AI Models Supported

Files Created

Test Results

Next Step
```
