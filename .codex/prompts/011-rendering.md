# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 011
## Video Rendering Pipeline Implementation


Version:

1.0.0


---

# ROLE

You are implementing the video production engine of ClipStudio AI.

Act as:

```
Video Processing Engineer

+

FFmpeg Specialist

+

Media Pipeline Architect
```

---

# OBJECTIVE

Build a production-grade video rendering system.

The renderer must:

```
Download Required Segment

Cut Video

Generate Subtitle

Apply Watermark

Render Final Output

Validate Quality
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/013-Rendering-System.md
```

---

# CORE PRINCIPLE

Optimize:

```
Quality

+

Speed

+

Storage Efficiency
```

Avoid:

```
Downloading Entire Videos
```

---

# TASK 1

Create Rendering Module

Location:

```
services/rendering/
```

Structure:

```
rendering/

├── engine.py

├── downloader.py

├── cutter.py

├── subtitle.py

├── watermark.py

├── encoder.py

├── validator.py

└── schemas.py
```

---

# TASK 2

Create Rendering Engine

Responsibilities:

```
Receive Clip Candidate

Prepare Assets

Render Output

Validate Result
```

---

# TASK 3

Create Partial Download System

Support:

```
Timestamp Range Download
```

Input:

```
Start Time

End Time
```

Output:

```
Required Video Segment
```

---

# TASK 4

Create Downloader Interface

Support:

```
Local Files

Remote Sources

Future Providers
```

Interface:

```
download_segment()

validate_source()

cleanup()
```

---

# TASK 5

Create FFmpeg Pipeline

Support:

```
Cutting

Encoding

Filtering

Muxing
```

---

# TASK 6

Implement Video Cutting

Input:

```
Source Video

Timestamp Range
```

Output:

```
Clip File
```

---

# TASK 7

Create Subtitle Generator

Support:

```
Transcript Segments

Timestamp Alignment

Subtitle Styling
```

Output:

```
SRT

ASS

Embedded Subtitle
```

---

# TASK 8

Create Subtitle Style System

Configurable:

```
Font

Size

Position

Color

Animation
```

---

# TASK 9

Create Watermark System

Support:

```
Image Watermark

Text Watermark

Position

Opacity
```

---

# TASK 10

Agent Watermark Integration

Agent configuration controls:

```
Watermark

Style

Position
```

---

# TASK 11

Create Aspect Ratio Converter

Support:

```
9:16 Vertical

16:9 Landscape

1:1 Square
```

---

# TASK 12

Create Smart Crop System

Prepare:

```
Face Detection

Subject Tracking

Center Crop
```

---

# TASK 13

Create Encoder Configuration

Support:

```
Resolution

Bitrate

FPS

Codec
```

---

# TASK 14

Create Quality Validator

Check:

```
Video Exists

Duration Correct

Audio Exists

Resolution Valid
```

---

# TASK 15

Create Render Metadata

Store:

```
Source

Timestamp

Settings

Model Version

Agent
```

---

# TASK 16

Create Rendering Events

Publish:

```
RenderStarted

RenderProgress

RenderCompleted

RenderFailed
```

---

# TASK 17

Workflow Integration

Create task:

```
Render Clip
```

Input:

```
Selected Segment
```

Output:

```
Final Video
```

---

# TASK 18

Storage Integration

Save:

```
Rendered Video

Preview

Metadata
```

---

# TASK 19

Create API Integration

Prepare:

```
POST /clips/{id}/export
```

---

# TASK 20

Create Rendering Tests

Test:

```
Download Segment

Cut Video

Subtitle

Watermark

Render

Validation
```

---

# CODING RULES

Must:

```
Use FFmpeg Abstraction

Keep Pipeline Modular

Support Future Codecs
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Memory Usage

Temporary Files

Encoding Speed
```

Support:

```
GPU Acceleration
```

when available.

---

# SECURITY REQUIREMENTS

Protect:

```
Temporary Files

External URLs

File Paths
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Publishing Automation

Social Media Upload
```

User approval remains required.

---

# VALIDATION

Run:

```
Input Segment

Download

Render

Generate Subtitle

Apply Watermark

Validate Output
```

---

# SUCCESS CRITERIA

Prompt 011 complete when:

✓ Partial download works

✓ FFmpeg pipeline works

✓ Subtitle works

✓ Watermark works

✓ Quality validation works

✓ Workflow connected

---

# OUTPUT REPORT

Provide:

```
Rendering Architecture

FFmpeg Setup

Files Created

Test Results

Next Step
```
