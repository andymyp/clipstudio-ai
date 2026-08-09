"""Central API exception handlers."""

from typing import cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException

from ..core.exceptions import ClipStudioError
from ..schemas.common import ErrorDetail


def _error_response(
    request: Request, status_code: int, code: str, message: str
) -> JSONResponse:
    """Build a safe standard error envelope."""
    request_id = getattr(request.state, "request_id", None)
    body = {
        "success": False,
        "data": None,
        "error": ErrorDetail(
            code=code, message=message, request_id=request_id
        ).model_dump(),
    }
    return JSONResponse(status_code=status_code, content=body)


async def validation_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle invalid request data without leaking internals."""
    return _error_response(
        request, 422, "validation_error", "Request validation failed."
    )


async def http_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Normalize framework HTTP errors into the public envelope."""
    error = cast(HTTPException, exc)
    message = str(error.detail) if isinstance(error.detail, str) else "Request failed."
    return _error_response(
        request, error.status_code, f"http_{error.status_code}", message
    )


async def application_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle expected domain/application failures."""
    error = cast(ClipStudioError, exc)
    return _error_response(request, 400, error.code, error.message)


async def database_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle database failures with a retry-safe public message."""
    return _error_response(
        request, 503, "database_error", "Database operation unavailable."
    )


async def unknown_error_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected failures without exposing stack traces."""
    return _error_response(request, 500, "internal_error", "Internal server error.")


def register_exception_handlers(application: FastAPI) -> None:
    """Register all standard exception handlers."""
    application.add_exception_handler(RequestValidationError, validation_error_handler)
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(ClipStudioError, application_error_handler)
    application.add_exception_handler(SQLAlchemyError, database_error_handler)
    application.add_exception_handler(Exception, unknown_error_handler)
