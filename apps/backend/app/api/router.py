"""Versioned API router composition."""

from fastapi import APIRouter

from .v1.router import router as v1_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(v1_router)

__all__ = ["api_router"]
