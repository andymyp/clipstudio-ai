"""Replaceable security ports for the local application boundary."""

from collections.abc import Mapping
from hmac import compare_digest
from typing import Protocol


class TokenValidator(Protocol):
    """Port for validating a request token."""

    def validate(self, token: str) -> bool:
        """Return whether the supplied token is valid."""


class PermissionChecker(Protocol):
    """Port for checking an actor permission."""

    def allowed(self, permission: str) -> bool:
        """Return whether the current actor has a permission."""


class LocalTokenValidator:
    """Constant-time validator for an injected local token."""

    def __init__(self, expected_token: str | None) -> None:
        self._expected_token = expected_token

    def validate(self, token: str) -> bool:
        """Validate without logging or exposing token contents."""
        if not self._expected_token or not token:
            return False
        return compare_digest(token, self._expected_token)


class AllowListPermissionChecker:
    """Simple permission adapter backed by injected permissions."""

    def __init__(self, permissions: Mapping[str, bool] | None = None) -> None:
        self._permissions = dict(permissions or {})

    def allowed(self, permission: str) -> bool:
        """Return an explicit permission decision."""
        return self._permissions.get(permission, False)


class SecretProvider:
    """Read-only secret port; implementations must keep values out of logs."""

    def __init__(self, secrets: Mapping[str, str] | None = None) -> None:
        self._secrets = dict(secrets or {})

    def get(self, name: str) -> str | None:
        """Return a secret by name, if configured."""
        return self._secrets.get(name)
