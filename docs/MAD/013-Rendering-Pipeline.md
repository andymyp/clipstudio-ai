# ClipStudio AI
# Master Architecture Document

Document:
013-Rendering-Pipeline.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 003-Tech-Stack.md
- 006-Workflow Engine.md
- 008-Segment Downloader.md
- 011-Scoring Engine.md
- 012-Deduplication Engine.md

Referenced By:

- 014-Storage Architecture
- 015-Database Design
- 020-Logging & Monitoring
- 024-Testing Strategy

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Rendering Pipeline.

The Rendering Pipeline transforms selected video segments into final short-form videos.

Responsibilities:

- video formatting
- subtitle generation
- watermark application
- audio processing
- encoding
- preview generation
- output preparation

---

# 2. Rendering Philosophy

Rendering is the final production stage.

Input:

```
Selected Segment

+

Subtitle

+

Agent Configuration

+

Metadata
```

Output:

```
Ready-To-Review Short Video
```

---

# 3. Rendering Goals

The pipeline must:

✓ produce platform-ready videos

✓ minimize CPU/RAM usage

✓ maintain quality

✓ support customization

✓ support multiple output profiles

✓ run reliably on laptop hardware

---

# 4. Non Responsibilities

Rendering does NOT:

- discover videos
- analyze content
- select clips
- score candidates

---

# 5. Rendering Architecture

```
              Selected Clip

                   |

                   ▼

          Rendering Controller

                   |

      ┌────────────┼────────────┐

      ▼            ▼            ▼

 Video Engine   Subtitle     Watermark


      |

      ▼

 Encoding Engine

      |

      ▼

 Final Output
```

---

# 6. Rendering Engine

Primary technology:

```
FFmpeg
```

---

Responsibilities:

- cutting
- scaling
- encoding
- filtering
- audio processing
- subtitle burning

---

# 7. Rendering Workflow

```
Segment Received

↓

Validate Input

↓

Load Agent Config

↓

Prepare Subtitle

↓

Apply Video Filters

↓

Apply Watermark

↓

Encode

↓

Quality Check

↓

Store Result
```

---

# 8. Output Format

Default short-video format:

```
Container:

MP4


Video:

H.264


Audio:

AAC


Aspect Ratio:

9:16
```

---

# 9. Resolution Profiles

Default:

```
1080x1920
```

---

Low Resource Mode:

```
720x1280
```

---

Future:

```
4K Vertical
```

---

# 10. Aspect Ratio Conversion

Source videos may vary:

```
16:9

4:3

1:1
```

Converted to:

```
9:16
```

---

# 11. Smart Cropping

Strategy:

```
Detect Important Region

↓

Crop Center

↓

Adjust Frame
```

Future support:

- face tracking
- object tracking

---

# 12. Subtitle Pipeline

Subtitle source:

```
Transcript Pipeline
```

---

Process:

```
Transcript

↓

Subtitle Generator

↓

Style Formatter

↓

FFmpeg Overlay
```

---

# 13. Subtitle Style Configuration

Agent controls:

```
Font

Size

Color

Position

Animation
```

---

Example:

```
Large Bold Subtitle

Bottom Center

High Contrast
```

---

# 14. Subtitle Timing

Supported:

```
Sentence level

Word level
```

---

Word level enables:

- karaoke style captions
- dynamic highlighting

---

# 15. Watermark System

Watermark belongs to Agent.

Configuration:

```
Text

Image

Position

Opacity

Scale
```

---

Example:

```
@ClipStudioAI

Bottom Right

60% opacity
```

---

# 16. Audio Processing

Operations:

- normalization
- volume adjustment
- noise reduction

---

Default:

```
Normalize loudness
```

---

# 17. Encoding Profiles

Preset:

```
short-form-balanced
```

Parameters:

```
H264

CRF optimized

AAC audio
```

---

Fast Mode:

```
lower quality

faster rendering
```

---

Quality Mode:

```
higher quality

slower rendering
```

---

# 18. Hardware Acceleration

Detection:

```
GPU available?

↓

Use acceleration

↓

Otherwise CPU
```

---

Target:

AMD Radeon Integrated Graphics.

---

# 19. Render Queue

Rendering is managed by:

```
Workflow Engine
```

---

Default:

```
Maximum concurrent render:

1
```

Reason:

Protect 16GB RAM.

---

# 20. Preview Generation

Before final render:

Generate:

```
Low resolution preview
```

Purpose:

- quick review
- faster feedback

---

# 21. Quality Check

After rendering:

Validate:

```
File exists

Duration correct

Resolution correct

Audio exists

Video playable
```

---

# 22. Output Metadata Generation

Each render receives:

```
title

description

hashtags

source

agent

score
```

---

# 23. Output Folder Structure

Example:

```
workspace/

renders/

   approved/

   review/

   failed/
```

---

# 24. Render Cache

Prevent re-rendering.

Cache key:

```
segment_hash

subtitle_version

watermark_version

profile
```

---

# 25. Failure Handling

FFmpeg crash:

```
Retry

↓

Capture logs

↓

Mark failed
```

---

Disk full:

```
Pause rendering

Notify user
```

---

# 26. Performance Optimization

For:

```
Ryzen 5 7430U

16GB RAM
```

Rules:

- one render at a time
- avoid unnecessary transcoding
- reuse downloaded segments
- use hardware acceleration when available

---

# 27. Rendering Example

Input:

```
Podcast segment

15:20 - 16:10
```

Process:

```
Download Segment

↓

Generate Subtitle

↓

Vertical Crop

↓

Add Watermark

↓

Encode

↓

Generate Title

↓

Review Queue
```

---

# 28. Future Improvements

Possible:

- AI auto framing
- face tracking
- dynamic captions
- background removal
- automatic B-roll insertion
- music recommendation

---

# 29. Final Architecture

```
             Segment

                |

                ▼

       Rendering Controller

                |

     ┌──────────┼──────────┐

     ▼          ▼          ▼

  FFmpeg   Subtitle   Watermark


                |

                ▼

          Final Short Video

                |

                ▼

            User Review
```

---

# 30. Summary

Rendering Pipeline provides:

✓ Professional short video output

✓ Automatic subtitles

✓ Watermark support

✓ Platform-ready format

✓ Resource-efficient rendering

✓ Review workflow

The Rendering Pipeline is the final production stage of ClipStudio AI.

---

End of Document