"""Deployable application boundary tests."""

from apps.backend.app.main import app


def test_deployable_app_exports_fastapi_application() -> None:
    assert app.title == "ClipStudio AI"
