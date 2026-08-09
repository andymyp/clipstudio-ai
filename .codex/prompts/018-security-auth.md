# ClipStudio AI
# Implementation Prompt

## Prompt 018
## Security Authentication System Implementation


Version:

1.0.0


---

# ROLE

You are implementing the security foundation of ClipStudio AI.

Act as:

```
Security Engineer

+

Backend Architect

+

Application Security Specialist
```

---

# OBJECTIVE

Build a production-grade security layer.

The system must provide:

```
Authentication

Authorization

Access Control

Secret Management

Audit Logging
```

---

# SOURCE OF TRUTH

Read:

```
/docs/MAD

/docs/PRD

/docs/TTD/019-Security-System.md
```

---

# CORE PRINCIPLE

Security model:

```
Every Request

Must Be Verified

Before Access
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

├── tokens.py

├── permissions.py

├── roles.py

├── secrets.py

├── audit.py

└── schemas.py
```

---

# TASK 2

Create Authentication System

Support:

```
User Login

Session Management

Token Validation
```

---

# TASK 3

Create Identity Model

Store:

```
User ID

Email

Status

Created Date
```

---

# TASK 4

Create Token System

Support:

```
Access Token

Refresh Token

Token Expiration
```

---

# TASK 5

Create Password Security

Implement:

```
Password Hashing

Password Validation

Secure Storage
```

---

# TASK 6

Create Authorization System

Support:

```
Role Based Access Control
```

---

# TASK 7

Create User Roles

Prepare:

```
ADMIN

USER

VIEWER
```

---

# TASK 8

Create Resource Permissions

Protect:

```
Agents

Videos

Clips

Storage

Settings
```

---

# TASK 9

Create Agent Isolation

Ensure:

```
User A

Cannot Access

User B Resources
```

---

# TASK 10

Create API Security Middleware

Protect:

```
REST API

Internal Services

Sensitive Operations
```

---

# TASK 11

Create Secret Management

Handle:

```
API Keys

Model Credentials

Database Credentials
```

---

# TASK 12

Environment Security

Support:

```
Environment Variables

Secret Files

Encrypted Storage
```

---

# TASK 13

Create Audit Logging

Track:

```
User Action

System Action

Configuration Change

Security Event
```

---

# TASK 14

Create Security Events

Publish:

```
LoginSuccess

LoginFailed

PermissionDenied

CredentialChanged
```

---

# TASK 15

Create Rate Limiting

Protect:

```
API Abuse

Brute Force

Resource Exhaustion
```

---

# TASK 16

Create Input Validation

Protect against:

```
Invalid Data

Injection

Malformed Requests
```

---

# TASK 17

Create Security Monitoring

Track:

```
Failed Login

Suspicious Activity

Access Pattern
```

---

# TASK 18

Create API Integration

Prepare:

```
POST /auth/login

POST /auth/logout

POST /auth/refresh

GET /auth/me
```

---

# TASK 19

Create Security Tests

Test:

```
Authentication

Authorization

Token Expiry

Permission Rules

Audit Logging
```

---

# TASK 20

Create Documentation

Update:

```
docs/security-architecture.md
```

Include:

```
Authentication Flow

Permission Model

Security Rules
```

---

# CODING RULES

Must:

```
Never Store Plain Password

Validate Every Request

Follow Least Privilege
```

---

# PERFORMANCE REQUIREMENTS

Optimize:

```
Token Validation

Permission Checking

Audit Storage
```

---

# SECURITY REQUIREMENTS

Must protect:

```
User Data

Media Files

AI Configuration

Credentials
```

---

# DO NOT IMPLEMENT

Do not implement:

```
Payment System

Subscription Billing

External Identity Providers
```

---

# VALIDATION

Run:

```
Create User

Login

Generate Token

Access Protected Resource

Verify Audit Log
```

---

# SUCCESS CRITERIA

Prompt 018 complete when:

✓ Authentication works

✓ Authorization works

✓ Resource isolation works

✓ Audit logging works

✓ API protected

✓ Tests pass

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
