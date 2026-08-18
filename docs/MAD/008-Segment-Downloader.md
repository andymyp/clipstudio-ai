# ClipStudio AI
# Master Architecture Document

Document:
008-Segment-Downloader.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 002-Architecture-Principles.md
- 004-System-Architecture.md
- 006-Workflow-Engine.md
- 007-Discovery-Engine.md

Referenced By:

- 009-Transcript Pipeline
- 013-Rendering Pipeline
- 014-Storage Architecture
- 015-Database Design

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Segment Downloader.

The Segment Downloader is responsible for retrieving only the required portion of a source video after AI analysis determines valuable timestamps.

The system MUST avoid downloading complete videos by default.

---

# 2. Core Principle

Traditional workflow:

```
Download Full Video

↓

Analyze

↓

Cut Clip
```

ClipStudio AI workflow:

```
Discover

↓

Extract Understanding

↓

AI Select Timestamp

↓

Download Required Segment

↓

Process Clip
```

---

# 3. Goals

The Segment Downloader must:

✓ minimize bandwidth usage

✓ minimize storage usage

✓ reduce processing time

✓ support multiple sources

✓ support resume

✓ support caching

✓ support precise clipping

---

# 4. Non Goals

Segment Downloader does NOT:

- decide which moment is interesting
- perform AI scoring
- create subtitles
- render final output

Those responsibilities belong to other modules.

---

# 5. Architecture Overview

```
          AI Analysis

              |

              ▼

      Timestamp Selection

              |

              ▼

     Segment Downloader

              |

      ┌───────┼────────┐

      ▼       ▼        ▼

 Source   Cache    Validator

 Adapter

      |

      ▼

   FFmpeg

      |

      ▼

 Segment File
```

---

# 6. Input Definition

Segment Downloader receives:

```
SegmentRequest
```

Example:

```
{

video_id:

"abc123",

source:

"YouTube",

start_time:

195.4,

end_time:

243.8,

quality:

1080p,

format:

mp4

}
```

---

# 7. Timestamp Model

Time format:

```
seconds
```

Example:

```
Start:

03:15.400


End:

04:03.800
```

Stored internally:

```
195.4

243.8
```

---

# 8. Download Strategy

The system uses multiple strategies.

Priority:

```
1. Native Segment Access

2. Stream Copy

3. Partial Download

4. Controlled Temporary Download
```

---

# 9. Strategy 1

## Native Segment Access

Preferred method.

If source provides segmented streaming:

Examples:

- HLS
- DASH

The downloader retrieves only required segments.

Example:

```
Manifest

↓

Segment List

↓

Required Segments Only

↓

Merge
```

---

# 10. Strategy 2

## FFmpeg Stream Extraction

For compatible sources:

```
Source Stream

↓

FFmpeg

↓

Start Time

↓

End Time

↓

Output Clip
```

---

Advantages:

- fast
- minimal storage
- efficient

---

# 11. Strategy 3

## Partial Download

For HTTP range compatible sources.

Process:

```
Media Request

↓

Byte Range Calculation

↓

Download Required Bytes

↓

Reconstruct Segment
```

---

# 12. Strategy 4

## Temporary Controlled Download

Fallback only.

Used when:

- source does not support segments
- no range support
- encrypted stream

Rules:

- temporary storage only
- automatic cleanup
- never stored permanently

---

# 13. Downloader Interface

Internal interface:

```
ISegmentDownloader
```

Methods:

```
downloadSegment()

estimateSize()

checkSupport()

resume()

cancel()
```

---

# 14. Source Adapter Integration

Architecture:

```
ISourceAdapter

        |

        ▼

Segment Capability Detection

        |

        ▼

Downloader Strategy Selection
```

---

# 15. Keyframe Handling

Video compression uses keyframes.

Problem:

Exact cutting may require re-encoding.

Strategy:

```
Fast Mode:

Nearest keyframe


Quality Mode:

Frame accurate extraction
```

---

# 16. Extraction Modes

## Fast Mode

Use:

```
-stream copy
```

Advantages:

- very fast
- low CPU

Disadvantages:

- timestamp may shift slightly

---

## Quality Mode

Use:

```
re-encode
```

Advantages:

- frame accurate

Disadvantages:

- slower

---

# 17. Quality Selection

Default:

```
1080p

H264

AAC
```

Fallback:

```
720p
```

---

# 18. Cache Architecture

Segments are cached.

Example:

```
workspace/

cache/

segments/

video_id/

segment_hash.mp4
```

---

# 19. Cache Key

Generated from:

```
source_id

start_time

end_time

quality

format
```

Example:

```
hash(
youtube123
195
243
1080p
)
```

---

# 20. Duplicate Prevention

Before download:

Check:

```
Existing Segment Hash

↓

Reuse
```

---

# 21. Resume Download

Interrupted download:

```
Partial File

+

Download State

↓

Continue
```

---

# 22. Storage Lifecycle

Temporary:

```
downloads/temp
```

Processed:

```
workspace/clips
```

Final:

```
workspace/renders
```

---

# 23. Segment Validation

After download:

Validate:

```
File Exists

Duration Correct

Audio Exists

Video Exists

Checksum Valid
```

---

# 24. Error Handling

## Network Failure

Action:

Retry.

---

## Source Removed

Action:

Mark unavailable.

---

## Invalid Timestamp

Action:

Reject request.

---

## Corrupted Segment

Action:

Redownload.

---

# 25. Security Rules

Downloader must:

- validate URLs
- restrict output paths
- sanitize filenames
- prevent path traversal
- isolate external processes

---

# 26. Performance Optimization

For target laptop:

Ryzen 5 7430U

16 GB RAM

Rules:

```
Maximum download workers:

1-2


Maximum concurrent FFmpeg:

1
```

---

Avoid:

- storing temporary full videos
- unnecessary transcoding
- repeated downloads

---

# 27. Bandwidth Optimization

Techniques:

- metadata first
- subtitle first
- segment only
- cache reuse
- avoid duplicates

---

# 28. Segment Download Workflow

Example:

```
AI Analysis

↓

Found Best Moment:

15:20 - 16:05

↓

Segment Request

↓

Downloader Checks Capability

↓

Select Strategy

↓

Download Segment

↓

Validate

↓

Store

↓

Send To Renderer
```

---

# 29. Future Improvements

Possible:

- adaptive bitrate selection
- automatic quality selection
- distributed downloading
- CDN optimization
- cloud segment workers

---

# 30. Final Architecture

```
                 AI

                 |

                 ▼

        Timestamp Selection

                 |

                 ▼

        Segment Downloader

                 |

      ┌──────────┼──────────┐

      ▼          ▼          ▼

  Source     Cache      FFmpeg

 Adapter

      |

      ▼

 Generated Clip Segment
```

---

# 31. Summary

Segment Downloader provides:

✓ No full video download

✓ Minimal bandwidth usage

✓ Minimal storage usage

✓ Timestamp-based extraction

✓ Resume capability

✓ Cache reuse

✓ Source flexibility

✓ Laptop-friendly processing

This component is a core competitive advantage of ClipStudio AI.

---

End of Document