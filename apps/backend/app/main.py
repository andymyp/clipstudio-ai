"""Deployable entry point delegating to the canonical backend application."""

from backend.app.main import app, create_app

__all__ = ["app", "create_app"]
