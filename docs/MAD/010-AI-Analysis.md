# ClipStudio AI
# Master Architecture Document

Document:
010-AI-Analysis.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 002-Architecture-Principles.md
- 004-System Architecture.md
- 005-Agent Architecture.md
- 006-Workflow Engine.md
- 009-Transcript Pipeline.md

Referenced By:

- 011-Scoring Engine
- 012-Deduplication Engine
- 013-Rendering Pipeline
- 016-Vector Database

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Analysis Engine.

The AI Analysis Engine transforms raw video information into structured intelligence.

It determines:

- what the video is about
- what moments are important
- what emotions exist
- what stories are present
- what segments deserve further processing

---

# 2. AI Analysis Philosophy

ClipStudio AI does not blindly cut videos.

The system first understands content.

Process:

```
Video Metadata

+

Transcript

+

Visual Information

+

Agent Objective

        |

        ▼

AI Understanding

        |

        ▼

Candidate Moments
```

---

# 3. Responsibilities

AI Analysis handles:

✓ semantic understanding

✓ context extraction

✓ story analysis

✓ emotion analysis

✓ topic identification

✓ highlight detection

✓ candidate generation

✓ metadata generation

---

# 4. Non Responsibilities

AI Analysis does NOT:

- download videos
- render videos
- manage files
- schedule jobs

---

# 5. Architecture Overview

```
                 Input

                   |

        ┌──────────┼──────────┐

        ▼          ▼          ▼

 Transcript    Metadata    Vision Data


        |

        ▼

 Context Builder

        |

        ▼

 AI Reasoning Engine

        |

        ▼

 Analysis Result

        |

        ▼

 Scoring Engine
```

---

# 6. Analysis Input

AI receives:

## Transcript

Contains:

- text
- timestamps
- speaker information

---

## Metadata

Contains:

- title
- description
- channel
- category
- duration

---

## Agent Configuration

Contains:

- objective
- target audience
- scoring preferences
- content style

---

## Optional Vision Data

Contains:

- objects
- scenes
- frames
- OCR

---

# 7. Context Builder

Before sending to AI:

Raw data is transformed into structured context.

Example:

```
Video:

Podcast Interview


Topic:

AI Technology


Important Moments:

00:12:30

Guest reveals unexpected fact
```

---

# 8. AI Model Architecture

Multi-model approach:

```
              AI Analysis

                   |

        ┌──────────┼──────────┐

        ▼          ▼          ▼

       LLM       Vision    Embedding
```

---

# 9. LLM Role

Primary reasoning engine.

Used for:

- understanding
- summarization
- classification
- reasoning
- candidate generation

---

Recommended runtime:

```
Ollama
```

Models:

Default:

```
Qwen3 8B
```

Low memory:

```
Gemma 3 4B
```

---

# 10. Vision Analysis

Optional visual understanding.

Used for:

- scene context
- facial reaction
- objects
- visual events

Models:

```
Florence-2

Qwen Vision
```

---

# 11. Embedding Analysis

Used for:

- similarity
- duplicate detection
- semantic search

Technology:

```
LanceDB

+

BGE Embeddings
```

---

# 12. Analysis Pipeline

```
Transcript

↓

Chunking

↓

Context Creation

↓

LLM Analysis

↓

Candidate Extraction

↓

Emotion Detection

↓

Story Understanding

↓

Structured Output
```

---

# 13. Transcript Chunking

Long transcripts are divided.

Example:

```
Video:

2 hours


Chunks:

5 minutes each
```

Purpose:

- reduce context size
- improve accuracy
- lower RAM usage

---

# 14. Context Window Management

Rules:

Never send entire long video transcript blindly.

Use:

```
Relevant chunks

+

Metadata

+

Agent goal
```

---

# 15. Prompt Architecture

Prompts are layered.

Structure:

```
System Prompt

+

Agent Prompt

+

Analysis Task

+

Video Context

+

Expected Output Format
```

---

# 16. System Prompt

Defines:

- role
- behavior
- limitations

Example:

```
You are a professional short-form video analyst.
Find moments with high engagement potential.
```

---

# 17. Agent Prompt

Defines specialization.

Example:

Funny Agent:

```
Find humorous moments.
Prioritize surprise and reactions.
```

Motivation Agent:

```
Find emotional inspirational moments.
```

---

# 18. Structured Output

AI must return structured JSON.

Example:

```
{
moment:

"guest reaction",

start:

720,

end:

760,

reason:

"strong emotional response"
}
```

---

# 19. Candidate Moment Model

Example:

```
CandidateMoment

{

start_time,

end_time,

description,

topic,

emotion,

confidence

}
```

---

# 20. Emotion Analysis

Supported emotions:

```
happy

sad

surprise

anger

inspiration

fear

humor
```

---

# 21. Story Understanding

AI identifies:

- setup
- conflict
- climax
- resolution

Example:

```
Setup:

Problem introduced


Climax:

Unexpected answer


Resolution:

Audience reaction
```

---

# 22. Hook Detection

AI detects:

First seconds quality.

Signals:

- surprising statement
- question
- conflict
- strong emotion

---

# 23. Engagement Prediction

AI estimates:

```
Viewer retention

Comment potential

Share potential

Replay potential
```

---

# 24. Analysis Memory

Store:

- successful patterns
- rejected patterns
- user feedback

Used for future improvement.

---

# 25. AI Analysis Storage

SQLite stores:

```
analysis_result

candidate_moments

model_version

timestamp
```

---

# 26. Failure Handling

LLM failure:

Retry.

---

Invalid output:

Regenerate.

---

Low confidence:

Request secondary analysis.

---

# 27. Resource Optimization

For target laptop:

Rules:

```
One LLM inference at a time.

Unload unused models.

Use quantized models.

Cache results.
```

---

# 28. Analysis Workflow Example

Funny Agent:

```
Transcript

↓

Find jokes

↓

Detect reactions

↓

Analyze context

↓

Generate candidates

↓

Send to scoring
```

---

# 29. Future Capabilities

Possible:

- multimodal reasoning
- self-improving agents
- viewer simulation
- viral prediction model
- trend forecasting

---

# 30. Final Architecture

```
              Video Candidate

                    |

                    ▼

             Transcript Data

                    |

                    ▼

             Context Builder

                    |

                    ▼

              AI Reasoning

                    |

                    ▼

          Candidate Moments

                    |

                    ▼

            Scoring Engine
```

---

# 31. Summary

AI Analysis Engine provides:

✓ Content understanding

✓ Semantic reasoning

✓ Emotional understanding

✓ Highlight discovery

✓ Agent specialization

✓ AI-powered clip selection

It transforms ClipStudio AI from an automation pipeline into an intelligent content production system.

---

End of Document