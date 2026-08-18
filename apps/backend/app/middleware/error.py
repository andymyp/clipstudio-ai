"""Error capture middleware."""

from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ..core.logging import get_logger


class ErrorCaptureMiddleware(BaseHTTPMiddleware):
    """Log unexpected exceptions while leaving response policy to handlers."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            return await call_next(request)
        except Exception:
            get_logger("clipstudio.http").exception(
                "request_failed",
                extra={"event": "request_failed", "stage": request.url.path},
            )
            raise
