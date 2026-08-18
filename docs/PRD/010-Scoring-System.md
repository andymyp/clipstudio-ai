# ClipStudio AI
# Product Requirements Document

Document:

010-Scoring-System.md


Version:

1.0.0


Status:

Approved


---

# 1. Purpose

This document defines the scoring system requirements.

It describes:

- how clips are evaluated
- scoring factors
- ranking logic
- quality threshold

---

# 2. Feature Definition

Scoring System evaluates every clip candidate and assigns a quality score.

---

# 3. Scoring Goal

The system must answer:

```
Is this clip worth producing?
```

---

# 4. Scoring Pipeline

```
Clip Candidate

        |

        ▼

Feature Evaluation

        |

        ▼

Score Calculation

        |

        ▼

Ranking

        |

        ▼

Selection
```

---

# 5. Score Output

Every candidate receives:

```
Overall Score

Confidence Score

Score Explanation
```

---

Example:

```
Overall:

87/100


Reason:

Strong emotional hook and complete story.
```

---

# 6. Scoring Factors

Main factors:

```
Engagement Potential

Content Quality

Emotion

Context

Completeness

Originality
```

---

# 7. Engagement Score

Measures:

```
Audience Interest

Attention Trigger

Share Potential
```

---

Weight:

```
25%
```

---

# 8. Hook Score

Measures first seconds:

```
Strong Opening

Curiosity

Immediate Value
```

---

Weight:

```
20%
```

---

# 9. Emotion Score

Measures emotional impact:

```
Funny

Surprising

Inspiring

Interesting
```

---

Weight:

```
20%
```

---

# 10. Context Score

Measures:

```
Story Understanding

Completeness

Meaning
```

---

Weight:

```
15%
```

---

# 11. Information Score

Measures:

```
Knowledge Value

Unique Insight

Useful Content
```

---

Weight:

```
10%
```

---

# 12. Originality Score

Measures:

```
Not Previously Used

Unique Segment

Different Perspective
```

---

Weight:

```
10%
```

---

# 13. Agent-Based Scoring

Different agents may use different weights.

---

Example:

## Funny Agent

```
Humor

40%

Reaction

30%

Surprise

30%
```

---

## Educational Agent

```
Knowledge

50%

Clarity

30%

Interest

20%
```

---

# 14. Score Calculation

Example:

```
Final Score =

Hook

+

Emotion

+

Context

+

Quality

+

Originality
```

---

# 15. Quality Threshold

Default:

```
Minimum Score:

70/100
```

---

Below threshold:

```
Reject
```

---

Above threshold:

```
Continue Pipeline
```

---

# 16. Ranking System

Candidates sorted:

```
Highest Score

↓

Lowest Score
```

---

Example:

```
Clip A

92


Clip B

84


Clip C

71
```

---

# 17. Clip Selection Limit

Agent can define:

Example:

```
Generate:

5 clips/day
```

System selects:

```
Top 5
```

---

# 18. Score Explanation

Required.

User should see:

```
Why Selected

Strength

Weakness
```

---

# 19. Learning System

Future:

System improves using:

```
Approved Clips

Rejected Clips

User Feedback
```

---

# 20. Anti-Pattern Prevention

Avoid selecting clips because:

```
High Views Only

Popular Source Only

Random Cutting
```

---

# 21. Performance Optimization

Scoring should happen before:

```
Heavy Video Rendering
```

---

Purpose:

Save:

```
CPU

Storage

Processing Time
```

---

# 22. Failure Handling

Possible errors:

```
Missing Data

AI Failure

Invalid Score
```

---

Fallback:

```
Default Scoring Rules
```

---

# 23. Acceptance Criteria

Scoring System is complete when:

✓ Every candidate receives score

✓ Ranking works

✓ Low-quality clips are filtered

✓ User understands selection reason

---

# 24. Final Definition

Scoring System ensures ClipStudio AI produces:

```
Fewer

+

Better

+

More Valuable
```

clips.

---

End of Document