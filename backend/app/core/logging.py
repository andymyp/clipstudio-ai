"""Structured JSON logging with local file rotation."""

import json
import logging
import logging.handlers
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from app.core.config import Settings

trace_id: ContextVar[str] = ContextVar("trace_id", default="")


class JsonFormatter(logging.Formatter):
    """Serialize log records into stable JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "trace_id": trace_id.get() or None,
        }
        for key in ("event", "agent", "task_id", "stage", "duration", "result"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)


def configure_logging(settings: Settings) -> None:
    """Configure console and rotating application log handlers once."""
    log_path = Path(settings.storage.log_path)
    log_path.mkdir(parents=True, exist_ok=True)
    root = logging.getLogger()
    root.setLevel(logging.DEBUG if settings.app.debug else logging.INFO)
    if getattr(root, "_clipstudio_configured", False):
        return

    formatter = JsonFormatter()
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)
    file_handler = logging.handlers.RotatingFileHandler(
        log_path / "application.jsonl",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    root.addHandler(console)
    root.addHandler(file_handler)
    root._clipstudio_configured = True  # type: ignore[attr-defined]


def get_logger(name: str) -> logging.Logger:
    """Get a namespaced logger with a trace id available to callers."""
    if not trace_id.get():
        trace_id.set(str(uuid4()))
    return logging.getLogger(name)
