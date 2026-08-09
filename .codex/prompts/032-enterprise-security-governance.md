# ClipStudio AI
# Claude Code Implementation Prompt

## Prompt 032
## Security, Privacy & Governance Layer Implementation


Version:

1.0.0


---

# ROLE

You are implementing the security foundation of ClipStudio AI.

Act as:

```
Application Security Architect

+

Privacy Engineer

+

Security Infrastructure Engineer
```

---

# OBJECTIVE

Build a complete security and governance system.

The system must protect:

```
User Data

Media Files

AI Models

Credentials

System Operations
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD
```

---

# CORE PRINCIPLE

Security must be:

```
Local First

Privacy First

Zero Trust

User Controlled
```

---

# TASK 1

Create Security Module

Location:

```
services/security/
```

Structure:

```
security/

├── auth.py

├── permissions.py

├── encryption.py

├── secrets.py

├── audit.py

├── policies.py

└── schemas.py
```

---

# TASK 2

Create Identity System

Support:

```
Local User Account

Session Management

Authentication
```

---

# TASK 3

Create Role System

Roles:

```
Owner

Admin

User

Viewer
```

---

# TASK 4

Create Permission Framework

Control:

```
Agent Access

File Access

Model Access

System Actions
```

---

# TASK 5

Create Secure Credential Storage

Protect:

```
API Keys

Tokens

Secrets

Configurations
```

---

# TASK 6

Create Encryption Layer

Encrypt:

```
User Data

Preferences

Credentials

Private Media Metadata
```

---

# TASK 7

Create Local Data Isolation

Separate:

```
Users

Projects

Agents

Storage
```

---

# TASK 8

Create Audit Logging

Record:

```
User Action

Agent Action

System Event

Security Event
```

---

# TASK 9

Create Audit Viewer

Support:

```
Search Logs

Filter Events

Export Report
```

---

# TASK 10

Create AI Tool Permission System

Control:

```
Which Agent

Can Use Which Tool
```

Example:

```
Discovery Agent

Allowed:

Search

Metadata

Not Allowed:

Delete Files
```

---

# TASK 11

Create File Security Layer

Protect:

```
Imported Videos

Generated Clips

Model Files
```

---

# TASK 12

Create Privacy Controls

Allow:

```
Delete Data

Reset Learning

Clear History

Export Data
```

---

# TASK 13

Create Security Events

Publish:

```
LoginSuccess

PermissionDenied

SecretAccess

SecurityAlert
```

---

# TASK 14

Create Threat Detection

Detect:

```
Suspicious Access

Repeated Failure

Unexpected Operation
```

---

# TASK 15

Create Secure API Layer

Implement:

```
Authentication Middleware

Authorization Middleware

Request Validation
```

---

# TASK 16

Create Secure Agent Execution

Agents must have:

```
Limited Permissions

Tool Restrictions

Execution Boundary
```

---

# TASK 17

Create Backup Protection

Support:

```
Configuration Backup

Encrypted Export

Restore
```

---

# TASK 18

Create Security Tests

Test:

```
Authentication

Authorization

Encryption

Permission

Audit
```

---

# TASK 19

Create Security Documentation

Update:

```
docs/security-governance.md
```

Include:

```
Security Model

Permission System

Privacy Controls
```

---

# TASK 20

Create Security Review Checklist

Validate:

```
Data Protection

Access Control

Secret Management

Privacy
```

---

# CODING RULES

Must:

```
Never Store Plain Secrets

Least Privilege Principle

Secure By Default
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Encryption Overhead

Audit Storage

Permission Checks
```

---

# SECURITY REQUIREMENTS

Mandatory:

```
No Hardcoded Credentials

No Hidden Data Collection

No External Tracking
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Surveillance Features

User Tracking

Data Selling
```

---

# VALIDATION

Run:

```
Create User

Assign Permission

Access Resource

Generate Audit Log

Verify Protection
```

---

# SUCCESS CRITERIA

Prompt 032 complete when:

✓ Authentication works

✓ Permission system works

✓ Encryption works

✓ Audit trail works

✓ Privacy controls work

✓ Security tests pass

---

# OUTPUT REPORT

Provide:

```
Security Architecture

Permission Model

Files Created

Test Results

Next Step
```