# ClipStudio AI
# Master Architecture Document

Document:
011-Scoring-Engine.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 000-README.md
- 005-Agent-Architecture.md
- 006-Workflow Engine.md
- 010-AI Analysis.md

Referenced By:

- 008-Segment Downloader
- 013-Rendering Pipeline
- 015-Database Design
- 016-Vector Database

---

# 1. Purpose

This document defines the architecture of the ClipStudio AI Scoring Engine.

The Scoring Engine evaluates candidate video moments and ranks them based on their potential quality and engagement.

---

# 2. Scoring Philosophy

ClipStudio AI does not select clips randomly.

Every candidate receives a score.

Example:

```
Candidate A

Score:

91/100


Candidate B

Score:

64/100
```

Only high-scoring candidates continue.

---

# 3. Responsibilities

Scoring Engine handles:

✓ candidate ranking

✓ engagement prediction

✓ quality evaluation

✓ agent-specific evaluation

✓ confidence calculation

✓ final selection

---

# 4. Non Responsibilities

Scoring Engine does NOT:

- download videos
- edit videos
- render clips
- generate subtitles

---

# 5. Architecture Overview

```
             AI Analysis Result

                    |

                    ▼

             Scoring Engine

                    |

       ┌────────────┼────────────┐

       ▼            ▼            ▼

 Rule Score    AI Score    Similarity Score


       |

       ▼

 Final Ranking

       |

       ▼

 Selected Clips
```

---

# 6. Scoring Model

Hybrid approach:

```
AI Reasoning

+

Machine Rules

+

Historical Data
```

---

# 7. Score Components

Default scoring:

```
Total Score = 100
```

Components:

```
Hook Score          20%

Emotion Score       20%

Story Score         20%

Engagement Score    20%

Agent Match Score   10%

Quality Score       10%
```

---

# 8. Hook Score

Measures first seconds impact.

Signals:

- strong opening statement
- curiosity
- surprise
- question
- conflict

Example:

```
Opening:

"You won't believe what happened..."

Score:

95
```

---

# 9. Emotion Score

Measures emotional strength.

Signals:

```
Humor

Surprise

Sadness

Inspiration

Excitement
```

Example:

```
Strong reaction:

90
```

---

# 10. Story Score

Measures narrative quality.

Evaluates:

```
Beginning

↓

Development

↓

Payoff
```

---

High score:

Complete mini story.

---

Low score:

Context missing.

---

# 11. Engagement Score

Predicts viewer behavior.

Signals:

- comments
- shares
- replay possibility
- discussion potential

---

# 12. Agent Match Score

Each agent has different priorities.

Example:

Funny Agent:

```
Humor:

50%

Reaction:

30%

Surprise:

20%
```

---

Motivation Agent:

```
Inspiration:

50%

Emotion:

30%

Story:

20%
```

---

# 13. Quality Score

Evaluates technical quality.

Signals:

```
Audio clarity

Transcript confidence

Video availability

Visual quality
```

---

# 14. Dynamic Scoring

Weights are configurable.

Example:

Agent:

```
Podcast Highlight
```

Changes:

```
Story:

40%

Insight:

40%

Emotion:

20%
```

---

# 15. AI Scoring

LLM evaluates:

- context
- emotional impact
- audience appeal

Output:

JSON.

Example:

```
{
emotion_score:90,

hook_score:85,

reason:
"Strong unexpected answer"
}
```

---

# 16. Rule-Based Scoring

Deterministic rules.

Examples:

Duration:

```
30-90 seconds

+

10 points
```

---

Transcript confidence:

```
>90%

+

5 points
```

---

# 17. Historical Scoring

Future learning layer.

Uses:

- previous successful clips
- user feedback
- performance data

---

Example:

```
Similar clips performed well

+

15 points
```

---

# 18. Candidate Ranking

Process:

```
All Candidates

↓

Calculate Score

↓

Sort Descending

↓

Select Top N
```

---

Example:

Input:

```
500 candidates
```

Output:

```
Top 10 clips
```

---

# 19. Score Threshold

Minimum default:

```
75/100
```

Below:

```
Rejected
```

---

# 20. Confidence Score

Every result includes confidence.

Example:

```
Score:

88

Confidence:

0.91
```

---

# 21. Duplicate Impact

Similar clips reduce score.

Example:

```
Already processed content

↓

-30 points
```

---

# 22. User Feedback Integration

User actions:

```
Approve

Reject

Favorite

Delete
```

become signals.

---

# 23. Feedback Loop

```
Generated Clip

↓

User Decision

↓

Store Feedback

↓

Improve Future Score
```

---

# 24. Scoring Storage

SQLite:

Stores:

```
candidate_id

scores

weights

model_version

timestamp
```

---

# 25. Ranking Algorithm

Initial:

```
Weighted Sum
```

Future:

```
Learning-to-Rank Model
```

---

# 26. Performance Optimization

For laptop:

Use:

- batch scoring
- cached analysis
- lightweight models
- limited candidates

---

# 27. Example Scoring

Candidate:

Podcast joke moment.

Result:

```
Hook:

90


Emotion:

95


Story:

80


Engagement:

92


Agent Match:

95


Quality:

90
```

Final:

```
91/100
```

---

# 28. Workflow Integration

Pipeline:

```
AI Analysis

↓

Generate Candidates

↓

Scoring Engine

↓

Select Best

↓

Segment Download

↓

Render
```

---

# 29. Future Improvements

Possible:

- viral prediction model
- platform-specific scoring
- TikTok optimization
- YouTube Shorts optimization
- A/B testing

---

# 30. Final Architecture

```
          Candidate Moments

                  |

                  ▼

            Scoring Engine

                  |

      ┌───────────┼───────────┐

      ▼           ▼           ▼

    AI Score   Rules    History


                  |

                  ▼

             Ranked Clips
```

---

# 31. Summary

Scoring Engine provides:

✓ Intelligent ranking

✓ Agent-specific selection

✓ Engagement prediction

✓ Quality filtering

✓ Learning capability

✓ Reduced manual review

The Scoring Engine is the decision-making layer of ClipStudio AI.

---

End of Document