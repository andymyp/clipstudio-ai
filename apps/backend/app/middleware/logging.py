"""Request correlation and structured request logging middleware."""

from collections.abc import Awaitable, Callable
from time import perf_counter
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from ..core.logging import get_logger, trace_id


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Attach a request id and record method, path, status, and duration."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        trace_id.set(request_id)
        started = perf_counter()
        response = await call_next(request)
        duration_ms = round((perf_counter() - started) * 1000, 2)
        get_logger("clipstudio.http").info(
            "request_completed",
            extra={
                "event": "request_completed",
                "task_id": request_id,
                "stage": f"{request.method} {request.url.path}",
                "duration": duration_ms,
                "result": response.status_code,
            },
        )
        response.headers["X-Request-ID"] = request_id
        return response
