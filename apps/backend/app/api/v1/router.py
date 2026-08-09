"""Version one route composition."""

from fastapi import APIRouter

from ..health import router as health_router
from .agents import router as agents_router
from .clips import router as clips_router
from .models import router as models_router
from .settings import router as settings_router
from .system import router as system_router
from .videos import router as videos_router
from .workflows import router as workflows_router

router = APIRouter()
router.include_router(agents_router)
router.include_router(videos_router)
router.include_router(workflows_router)
router.include_router(clips_router)
router.include_router(models_router)
router.include_router(settings_router)
router.include_router(system_router)
router.include_router(health_router, prefix="/system")
