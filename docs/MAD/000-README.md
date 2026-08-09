# Master Architecture Document (MAD)

Version: 1.0.0

Project:
ClipStudio AI

Status:
Living Document

Last Updated:
2026

---

# Purpose

This document is the single source of truth for the entire ClipStudio AI architecture.

Every architectural decision must originate from this document.

The following documents depend on this MAD:

- PRD
- TTD
- Development Tasks
- Prompts
- AI Coding Instructions
- Testing Documents
- Deployment Documents
- Future ADR

No implementation may contradict this document.

---

# Vision

ClipStudio AI is a Local-First AI Operating System that automatically discovers long-form videos, analyzes them using AI, identifies the highest-value moments, downloads only the required video segments, generates subtitles, renders optimized short-form videos, and prepares them for human review before publishing.

The system is designed to:

- minimize storage usage
- minimize bandwidth usage
- maximize automation
- maximize extensibility
- maximize local privacy
- maximize processing efficiency

The user remains in complete control over the publishing process.

---

# Architecture Philosophy

ClipStudio AI follows these principles:

1.
Local First

Everything possible runs locally.

Cloud is optional.

No feature should require cloud unless explicitly enabled.

---

2.
AI Native

AI is the primary engine.

Traditional programming orchestrates AI.

---

3.
Pipeline Based

Everything is a pipeline.

Every stage produces structured outputs.

Every stage can be resumed.

---

4.
Composable

Every component can be replaced.

Every AI model can be swapped.

Every provider can be changed.

---

5.
Offline Friendly

Internet is required only for:

- discovering videos
- downloading video segments
- optional cloud AI

Everything else works offline.

---

6.
Resource Efficient

The target hardware is:

Windows 11

AMD Ryzen 5 7430U

16 GB RAM

Integrated Radeon Graphics

Architecture decisions must prioritize efficient CPU and memory usage.

---

7.
Deterministic

Every pipeline execution must be reproducible.

Same input

↓

Same output

---

8.
Stateless Services

AI workers should be stateless.

Only storage owns persistent state.

---

9.
Human In Control

Publishing is never automatic.

Users always review generated clips.

---

10.
Enterprise Quality

The architecture must support:

- plugins

- multiple AI providers

- multiple agents

- future cloud execution

without redesign.

---

# Core Workflow

Discovery

↓

Metadata

↓

Transcript

↓

AI Analysis

↓

Timestamp Selection

↓

Segment Download

↓

Subtitle

↓

Rendering

↓

Quality Check

↓

Review

↓

Manual Publish

---

# Core Design Decisions

## No Full Video Download

Videos are never downloaded entirely unless explicitly requested.

The system downloads only the required segment.

Reason:

- storage efficiency

- bandwidth efficiency

- faster processing

---

## Local Database

SQLite

WAL Mode

---

## Analytics

DuckDB

---

## Vector Search

LanceDB

---

## Rendering

FFmpeg

---

## Transcript

faster-whisper

---

## Desktop

Tauri v2

React

TypeScript

---

## Core

Rust

---

## AI

Python

FastAPI

---

## Scheduler

Tokio

---

## Config

TOML

---

## UI

shadcn/ui

Tailwind CSS

---

## State

Zustand

TanStack Query

---

# Repository Structure

/docs

/MAD

/PRD

/TTD

/prompts

/src

/apps

/packages

/models

/workspace

---

# Documentation Order

Read documents in this order:

000 README

001 Vision

002 Architecture Principles

003 Technology Stack

004 System Architecture

005 Agent Architecture

...

025 ADR

---

# Rules

Every architecture change requires:

- ADR

- version bump

- changelog

- review

No exception.

---

End of Document