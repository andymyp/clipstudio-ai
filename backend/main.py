"""Development entry point for ``python -m backend.main``."""

import sys
from pathlib import Path

BACKEND_PATH = Path(__file__).resolve().parent
if str(BACKEND_PATH) not in sys.path:
    sys.path.insert(0, str(BACKEND_PATH))


def main() -> None:
    """Start the development server from the repository root."""
    import uvicorn

    from backend.app.core.config import get_settings

    settings = get_settings()
    uvicorn.run(
        "backend.app.main:app",
        host=settings.app.host,
        port=settings.app.port,
        reload=settings.app.debug,
    )


if __name__ == "__main__":
    main()
