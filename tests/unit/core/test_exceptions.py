"""Exception taxonomy tests."""

from backend.app.core.exceptions import ProcessingError, ValidationError


def test_domain_error_keeps_recovery_context() -> None:
    error = ProcessingError("render failed", recovery="retry the render stage")

    assert error.code == "processing_error"
    assert error.message == "render failed"
    assert error.recovery == "retry the render stage"


def test_validation_error_has_stable_code() -> None:
    assert ValidationError("bad input").code == "validation_error"
