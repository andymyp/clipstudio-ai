# ClipStudio AI
# Master Architecture Document

Document:
018-Configuration.md

Version:
1.0.0

Status:
Approved

Dependencies:

- 003-Tech-Stack.md
- 005-Agent Architecture.md
- 014-Storage Architecture.md
- 017-Scheduler.md

Referenced By:

- 019-Model Management
- 023-Deployment
- 024-Testing Strategy

---

# 1. Purpose

This document defines the configuration architecture of ClipStudio AI.

Configuration controls:

- application behavior
- AI models
- agents
- storage
- scheduling
- performance
- security

---

# 2. Configuration Philosophy

ClipStudio AI separates:

```
Application Logic

AND

User Configuration
```

---

# 3. Configuration Sources

Priority order:

```
1. Runtime Settings

2. User Configuration

3. Default Configuration

4. Environment Variables
```

---

# 4. Configuration Architecture

```
                 Config System

                      |

      ┌───────────────┼───────────────┐

      ▼               ▼               ▼

 Application       Agents          Models


      |

      ▼

 Performance
```

---

# 5. Configuration Format

Primary:

```
YAML
```

Reason:

- human readable
- easy editing
- supports hierarchy

---

# 6. Configuration Directory

Structure:

```
config/

├── app.yaml

├── agents/

│   ├── funny.yaml

│   └── motivation.yaml

├── models.yaml

├── storage.yaml

└── performance.yaml
```

---

# 7. Application Configuration

File:

```
app.yaml
```

Example:

```
application:

name:

ClipStudio AI


mode:

local


language:

id
```

---

# 8. Agent Configuration

Each agent has:

```
agent.yaml
```

Example:

```
agent:

name:

Funny Moment Agent


enabled:

true
```

---

# 9. Agent Parameters

Configuration:

```
category

objective

sources

keywords

scoring

watermark

schedule

output
```

---

# 10. Source Configuration

Example:

```
sources:

youtube:

enabled:true


tiktok:

enabled:true
```

---

# 11. AI Configuration

Controls:

```
LLM model

embedding model

whisper model

vision model
```

---

# 12. Model Configuration

Example:

```
models:

llm:

qwen3-8b


embedding:

bge-small


speech:

whisper-small
```

---

# 13. Storage Configuration

Controls:

```
workspace location

cache size

cleanup policy

retention
```

---

Example:

```
storage:

workspace:

D:/ClipStudioAI


cache_limit:

20GB
```

---

# 14. Scheduler Configuration

Controls:

```
worker count

agent schedule

retry policy
```

---

Example:

```
scheduler:

workers:

2


retry:

3
```

---

# 15. Performance Profile

Profiles:

```
LOW

BALANCED

QUALITY
```

---

# 16. LOW Profile

Target:

Older hardware.

Settings:

```
small models

720p render

1 worker
```

---

# 17. BALANCED Profile

Default:

```
Ryzen 5 7430U

16GB RAM
```

Settings:

```
small/medium models

1080p render

1-2 workers
```

---

# 18. QUALITY Profile

Higher hardware.

Settings:

```
larger models

higher resolution

more processing
```

---

# 19. Runtime Configuration

Temporary overrides.

Example:

```
Run Agent

--quality-mode
```

---

# 20. Environment Variables

Sensitive values only.

Example:

```
.env
```

Contains:

```
API_KEYS

TOKENS

SECRETS
```

---

# 21. Configuration Validation

Every config must pass:

```
Schema Validation

↓

Type Check

↓

Dependency Check
```

---

# 22. Invalid Configuration

Action:

```
Reject

↓

Show Error

↓

Use Previous Valid Config
```

---

# 23. Configuration Versioning

Every config contains:

```
version:

1.0
```

---

Purpose:

Migration support.

---

# 24. Configuration Migration

Example:

```
config_v1

↓

Migration Script

↓

config_v2
```

---

# 25. User Settings

Stored:

```
settings table
```

Examples:

```
theme

language

default profile

notification
```

---

# 26. Agent Import / Export

Supported.

Example:

Export:

```
funny-agent.yaml
```

Import:

```
Install Agent
```

---

# 27. Security Rules

Never store:

```
API keys

Passwords

Tokens
```

inside YAML.

---

Use:

```
.env

Encrypted Storage
```

---

# 28. Configuration Backup

Backup:

```
agents/

config/

database/settings
```

---

# 29. Performance Optimization

Configuration controls:

```
model size

workers

quality

cache
```

---

# 30. Example Complete Flow

```
User Creates Agent

↓

Agent YAML Created

↓

Scheduler Reads Config

↓

Workflow Uses Config

↓

AI Models Selected

↓

Output Generated
```

---

# 31. Final Architecture

```
             Configuration

                    |

      ┌─────────────┼─────────────┐

      ▼             ▼             ▼

   Agents        Models       Runtime


                    |

                    ▼

              Application
```

---

# 32. Summary

Configuration Architecture provides:

✓ Flexible customization

✓ Agent-based behavior

✓ Hardware optimization

✓ Easy deployment

✓ Migration support

✓ Separation of code and settings

Configuration is the control layer of ClipStudio AI.

---

End of Document