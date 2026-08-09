"""Versioned API router composition."""

from fastapi import APIRouter

from .health import router as health_router
from .system import router as system_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router, prefix="/system")
api_router.include_router(system_router)

__all__ = ["api_router"]
