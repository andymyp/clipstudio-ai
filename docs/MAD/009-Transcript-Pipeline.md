# ClipStudio AI
# Master Architecture Document

Document:
009-Transcript-Pipeline.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 002-Architecture-Principles.md
- 003-Tech-Stack.md
- 006-Workflow-Engine.md
- 007-Discovery-Engine.md
- 008-Segment-Downloader.md

Referenced By:

- 010-AI Analysis
- 011-Scoring Engine
- 015-Database Design
- 016-Vector Database

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Transcript Pipeline.

The Transcript Pipeline converts video speech into structured text with timestamps.

The transcript becomes the primary input for:

- AI understanding
- highlight detection
- semantic search
- scoring
- clip selection

---

# 2. Transcript Philosophy

Traditional workflow:

```
Download Video

↓

Watch Video

↓

Understand Content
```

ClipStudio AI workflow:

```
Metadata

↓

Transcript

↓

AI Understanding

↓

Timestamp Selection

↓

Download Segment
```

---

# 3. Goals

Transcript Pipeline must:

✓ minimize video processing

✓ support multiple languages

✓ provide timestamp alignment

✓ support local inference

✓ provide searchable content

✓ enable AI reasoning

✓ support caching

---

# 4. Non Goals

Transcript Pipeline does NOT:

- decide clip quality
- render subtitles
- select final clips
- perform video editing

---

# 5. Architecture Overview

```
              Video Source

                   |

                   ▼

          Subtitle Discovery

                   |

        ┌──────────┴──────────┐

        ▼                     ▼

 Official Subtitle       Speech Recognition


        |

        ▼

 Transcript Normalizer

        |

        ▼

 Transcript Storage

        |

        ▼

 AI Analysis Engine
```

---

# 6. Transcript Source Priority

The system uses this priority:

```
1. Official Subtitle

2. Platform Auto Subtitle

3. Existing Transcript

4. faster-whisper
```

---

# 7. Subtitle Extraction

When available:

Extract:

- language
- timestamps
- text
- confidence

No AI processing required.

---

# 8. Speech Recognition Engine

Primary:

```
faster-whisper
```

---

Why:

- optimized Whisper implementation
- lower memory usage
- faster inference

---

# 9. Whisper Model Strategy

Default:

```
small
```

---

High Quality:

```
medium
```

---

Low Resource:

```
tiny
base
```

---

# 10. Hardware Optimization

Target:

```
Ryzen 5 7430U

16GB RAM
```

Recommended:

```
small model

CPU inference

limited workers
```

---

# 11. Audio Processing Flow

When Whisper is required:

```
Video Segment

↓

Extract Audio

↓

Normalize Audio

↓

Whisper

↓

Transcript
```

---

# 12. Audio Extraction

Technology:

```
FFmpeg
```

Process:

```
Input Video

↓

16kHz mono audio

↓

Whisper
```

---

# 13. Transcript Data Model

Example:

```
Transcript

{

video_id,

language,

segments[]

}
```

---

Segment:

```
{

start:

120.5,


end:

128.7,


text:

"example sentence",

confidence:

0.92

}
```

---

# 14. Word Level Timestamp

Supported.

Example:

```
word:

"important"

start:

123.1

end:

123.8
```

Used for:

- accurate subtitles
- precise clipping
- highlight detection

---

# 15. Transcript Normalization

All transcripts converted into common format.

Normalization:

- remove duplicate spaces
- fix punctuation
- detect language
- normalize timestamps

---

# 16. Language Detection

Detected:

```
English

Indonesian

Japanese

etc.
```

Used for:

- model selection
- subtitle generation
- translation

---

# 17. Translation Support

Future capability:

```
Original Transcript

↓

Translation Model

↓

Translated Transcript
```

Example:

English video

↓

Indonesian subtitle

---

# 18. Transcript Storage

Primary:

SQLite

---

Stored:

```
video

language

segments

timestamps

confidence

status
```

---

# 19. Transcript Cache

Before processing:

Check:

```
Existing Transcript

↓

Reuse
```

---

Cache key:

```
video_id

language

model_version
```

---

# 20. Transcript Events

Generated:

```
TranscriptStarted

TranscriptCompleted

TranscriptFailed
```

---

# 21. Transcript Quality Validation

Checks:

```
Text length

Timestamp validity

Confidence score

Language detection
```

---

# 22. Confidence Handling

Low confidence:

```
Request better model

or

mark uncertain
```

---

# 23. Transcript Pipeline Workflow

Example:

```
Candidate Video

↓

Check Subtitle

↓

Subtitle Found?

       |

      Yes

       |

       ▼

Normalize


       |

      No

       |

       ▼

Extract Audio

       |

       ▼

Whisper

       |

       ▼

Store Transcript

       |

       ▼

AI Analysis
```

---

# 24. Failure Handling

## Missing Audio

Action:

Reject.

---

## Whisper Failure

Action:

Retry.

---

## Invalid Subtitle

Action:

Fallback Whisper.

---

# 25. Performance Optimization

Techniques:

- reuse transcripts
- process audio only
- batch operations
- unload models after inactivity

---

# 26. Memory Management

Rules:

Only one speech model loaded.

Example:

```
Whisper

OR

Vision

OR

LLM
```

Avoid simultaneous large models.

---

# 27. Integration With AI Analysis

Transcript provides:

```
Content

Context

Timeline

Keywords

Emotion clues
```

AI Analysis consumes:

```
Transcript

+

Metadata

+

Agent Rules
```

---

# 28. Future Improvements

Possible:

- speaker diarization
- emotion detection from voice
- automatic chaptering
- conversation mapping
- voice quality analysis

---

# 29. Final Architecture

```
              Video

                |

                ▼

          Subtitle Check

                |

        ┌───────┴────────┐

        ▼                ▼

 Subtitle           Whisper

        |

        ▼

 Transcript Store

        |

        ▼

 AI Analysis
```

---

# 30. Summary

Transcript Pipeline provides:

✓ Efficient video understanding

✓ No full video processing

✓ Timestamp-aware text

✓ Local AI capability

✓ Searchable content

✓ AI-ready information

Transcript Pipeline is the foundation of intelligent clip discovery.

---

End of Document