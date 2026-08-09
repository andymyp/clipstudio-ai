# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 008
## Transcript AI Pipeline Implementation


Version:

1.0.0


---

# ROLE

You are implementing the speech intelligence layer of ClipStudio AI.

Act as:

```
AI Speech Engineer

+

Machine Learning Engineer

+

Backend Engineer
```

---

# OBJECTIVE

Build a transcript extraction system.

The system must:

```
Extract Speech

Convert To Text

Generate Timestamps

Detect Language

Prepare AI Analysis Input
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/009-Transcript-System.md
```

---

# CORE PRINCIPLE

Transcript pipeline:

```
Understand Content

Before

Heavy Processing
```

---

# TASK 1

Create Transcript Module

Location:

```
services/transcript/
```

Structure:

```
transcript/

├── engine.py

├── extractor.py

├── providers.py

├── alignment.py

├── language.py

├── cleaner.py

└── schemas.py
```

---

# TASK 2

Create Transcript Engine

Responsibilities:

```
Receive Video Source

Extract Speech

Generate Transcript

Store Result
```

---

# TASK 3

Create Speech Provider Interface

Support:

```
Local Model

External API

Future Providers
```

Interface:

```
transcribe()

detect_language()

health_check()
```

---

# TASK 4

Prepare Speech Models

Architecture support:

```
Whisper

Faster Whisper

Other STT Models
```

Do not hardcode provider.

---

# TASK 5

Create Audio Extraction Pipeline

Support:

```
Video URL

Local File

Partial Audio Extraction
```

---

# TASK 6

Create Timestamp System

Store:

```
Start Time

End Time

Text Segment
```

Example:

```
[
{
start:0.0,

end:3.5,

text:"..."
}
]
```

---

# TASK 7

Create Language Detection

Detect:

```
Language

Confidence Score
```

---

# TASK 8

Create Transcript Cleaning

Process:

```
Remove Noise

Normalize Text

Fix Formatting
```

---

# TASK 9

Create Transcript Storage Integration

Save:

```
Transcript

Segments

Language

Metadata
```

---

# TASK 10

Create Transcript Search Interface

Support:

```
Keyword Search

Semantic Search Ready
```

---

# TASK 11

Create Segment Extraction Support

Provide:

```
Timestamp Range
```

for:

```
Future Clip Generation
```

---

# TASK 12

Create AI Analysis Input Format

Output:

```
Video Context

Transcript

Timestamps
```

---

# TASK 13

Create Workflow Integration

Support task:

```
Extract Transcript
```

Input:

```
Video Candidate
```

Output:

```
Transcript Result
```

---

# TASK 14

Create Event Integration

Publish:

```
TranscriptStarted

TranscriptCompleted

TranscriptFailed
```

---

# TASK 15

Create Transcript Cache

Avoid:

```
Repeated Processing
```

Use:

```
Content Hash
```

---

# TASK 16

Create API Foundation

Prepare:

```
GET /videos/{id}/transcript
```

---

# TASK 17

Create Error Handling

Handle:

```
No Audio

Unsupported Language

Provider Failure

Timeout
```

---

# TASK 18

Create Transcript Tests

Test:

```
Audio Input

Text Output

Timestamp Accuracy

Storage

Failure Handling
```

---

# TASK 19

Create Example Pipeline

Flow:

```
Video Candidate

↓

Transcript

↓

Analysis Ready
```

---

# TASK 20

Create Documentation

Update:

```
docs/transcript-pipeline.md
```

Include:

```
Architecture

Providers

Data Flow
```

---

# CODING RULES

Must:

```
Use Provider Pattern

Keep Models Replaceable

Use Async Processing
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
CPU Usage

Memory

Batch Processing
```

Support:

```
GPU Acceleration When Available
```

---

# SECURITY REQUIREMENTS

Protect:

```
Temporary Audio Files

Local Data

External Credentials
```

---

# DO NOT IMPLEMENT

Do not implement:

```
AI Scoring

Video Rendering

Subtitle Rendering
```

---

# VALIDATION

Run:

```
Process Sample Video

Generate Transcript

Verify Timestamp

Store Result

Publish Event
```

---

# SUCCESS CRITERIA

Prompt 008 complete when:

✓ Transcript engine works

✓ STT provider interface exists

✓ Timestamp alignment works

✓ Workflow integrated

✓ Transcript stored

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Transcript Architecture

Providers

Files Created

Test Results

Next Step
```
