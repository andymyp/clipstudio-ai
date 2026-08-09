# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 012
## Storage Architecture Implementation


Version:

1.0.0


---

# ROLE

You are implementing the storage infrastructure layer of ClipStudio AI.

Act as:

```
Storage Architect

+

Backend Engineer

+

Media Infrastructure Engineer
```

---

# OBJECTIVE

Build a reliable local-first storage system.

The storage system must manage:

```
Videos

Clips

Metadata

Temporary Files

AI Assets

Logs
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/014-Storage-System.md
```

---

# CORE PRINCIPLE

Storage lifecycle:

```
Acquire

↓

Process

↓

Validate

↓

Store

↓

Cleanup
```

---

# TASK 1

Create Storage Module

Location:

```
services/storage/
```

Structure:

```
storage/

├── manager.py

├── filesystem.py

├── lifecycle.py

├── cleanup.py

├── metadata.py

├── checksum.py

└── schemas.py
```

---

# TASK 2

Create Storage Manager

Responsibilities:

```
Save Files

Read Files

Delete Files

Track Usage
```

---

# TASK 3

Create Storage Configuration

Support:

```
Storage Path

Maximum Size

Cleanup Policy

Retention Policy
```

---

# TASK 4

Create Directory Structure

Implement:

```
storage/

├── sources/

├── processing/

├── clips/

├── previews/

├── subtitles/

├── thumbnails/

├── models/

└── temp/
```

---

# TASK 5

Create File Metadata System

Store:

```
Filename

Path

Size

Hash

Type

Created Date
```

---

# TASK 6

Create Checksum System

Calculate:

```
File Hash

Content Hash
```

Purpose:

```
Duplicate Detection

Integrity Check
```

---

# TASK 7

Create Duplicate Prevention

Before saving:

Check:

```
Existing Hash

Existing Content
```

---

# TASK 8

Create Temporary File Manager

Manage:

```
Download Temp

Render Temp

Audio Temp
```

Support:

```
Automatic Cleanup
```

---

# TASK 9

Create File Lifecycle

States:

```
CREATED

PROCESSING

READY

ARCHIVED

DELETED
```

---

# TASK 10

Create Storage Quota System

Track:

```
Total Usage

Per Agent Usage

Temporary Usage
```

---

# TASK 11

Create Cleanup Worker

Cleanup:

```
Expired Files

Failed Processing Files

Unused Assets
```

---

# TASK 12

Create Media Organization

Organize:

```
Agent

Workflow

Clip

Date
```

Example:

```
clips/

agent-id/

2026/

08/

clip.mp4
```

---

# TASK 13

Create Preview Generator Interface

Prepare:

```
Thumbnail

Preview Video

Contact Sheet
```

---

# TASK 14

Create Storage Repository Integration

Support:

```
Store Metadata

Retrieve Metadata

Update Status
```

---

# TASK 15

Create Workflow Integration

Storage tasks:

```
Save Source

Save Render

Cleanup Temp
```

---

# TASK 16

Create Storage Events

Publish:

```
FileStored

FileDeleted

CleanupCompleted

StorageWarning
```

---

# TASK 17

Create API Integration

Prepare:

```
GET /storage/status

GET /clips/{id}/files
```

---

# TASK 18

Create Backup Preparation

Support future:

```
External Storage

Cloud Backup

Archive
```

---

# TASK 19

Create Storage Tests

Test:

```
Save File

Read File

Checksum

Duplicate Detection

Cleanup
```

---

# TASK 20

Create Documentation

Update:

```
docs/storage-architecture.md
```

Include:

```
Directory Structure

Lifecycle

Cleanup Rules
```

---

# CODING RULES

Must:

```
Abstract Storage Layer

Avoid Hardcoded Paths

Support Future Cloud Storage
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Disk Usage

File Access

Cleanup Speed
```

---

# SECURITY REQUIREMENTS

Protect:

```
File Paths

Temporary Data

Access Permissions
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Cloud Upload

Social Publishing

User Sharing
```

---

# VALIDATION

Run:

```
Store Video

Generate Metadata

Check Hash

Cleanup Temp

Verify Storage Status
```

---

# SUCCESS CRITERIA

Prompt 012 complete when:

✓ Storage manager works

✓ File lifecycle works

✓ Duplicate prevention works

✓ Cleanup works

✓ Workflow connected

✓ Tests pass

---

# OUTPUT REPORT

Provide:

```
Storage Architecture

Directory Layout

Files Created

Test Results

Next Step
```
