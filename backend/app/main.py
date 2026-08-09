"""Compatibility export for the deployable application factory."""

from collections.abc import Callable
from importlib import import_module
from typing import cast

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Load the deployable factory without creating a second application."""
    module = import_module("apps.backend.app.main")
    factory = cast(Callable[[], FastAPI], module.create_app)
    return factory()


app = create_app()

__all__ = ["app", "create_app"]
