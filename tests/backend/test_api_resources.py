"""Contract tests for the versioned REST resource surface."""

from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from apps.backend.app.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Run API requests through the production application factory."""
    with TestClient(create_app()) as test_client:
        yield test_client


def test_agent_lifecycle_uses_standard_envelopes(client: TestClient) -> None:
    """Agent CRUD and control actions expose the documented response shape."""
    payload = {
        "name": f"API test agent {uuid4()}",
        "category": "testing",
        "description": "Created by the REST contract test.",
    }
    created = client.post("/api/v1/agents", json=payload)
    assert created.status_code == 201
    body = created.json()
    assert body["success"] is True
    assert body["data"]["name"] == payload["name"]
    agent_id = body["data"]["id"]

    try:
        fetched = client.get(f"/api/v1/agents/{agent_id}")
        assert fetched.status_code == 200
        assert fetched.json()["data"]["status"] == "inactive"

        updated = client.put(
            f"/api/v1/agents/{agent_id}", json={"name": "Updated API test agent"}
        )
        assert updated.status_code == 200
        assert updated.json()["data"]["name"] == "Updated API test agent"

        activated = client.post(f"/api/v1/agents/{agent_id}/activate")
        assert activated.status_code == 200
        assert activated.json()["data"]["status"] == "active"

        paused = client.post(f"/api/v1/agents/{agent_id}/pause")
        assert paused.status_code == 200
        assert paused.json()["data"]["status"] == "paused"

        queued = client.post(f"/api/v1/agents/{agent_id}/run")
        assert queued.status_code == 202
        assert queued.json()["data"]["status"] == "queued"

        listed = client.get("/api/v1/agents", params={"limit": 1, "offset": 0})
        assert listed.status_code == 200
        assert listed.json()["data"]["limit"] == 1
        assert listed.json()["data"]["returned"] <= 1
    finally:
        deleted = client.delete(f"/api/v1/agents/{agent_id}")
        assert deleted.status_code == 200
        assert deleted.json() == {
            "success": True,
            "data": {"deleted": True},
            "error": None,
            "message": None,
        }

    missing = client.get(f"/api/v1/agents/{agent_id}")
    assert missing.status_code == 404
    assert missing.json()["success"] is False
    assert missing.json()["error"]["code"] == "http_404"


def test_api_validation_and_authentication_errors_are_normalized(
    client: TestClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Invalid payloads and configured local-token failures use one error shape."""
    invalid = client.post("/api/v1/agents", json={"name": ""})
    assert invalid.status_code == 422
    assert invalid.json()["success"] is False
    assert invalid.json()["error"]["code"] == "validation_error"

    monkeypatch.setenv("CLIPSTUDIO_LOCAL_TOKEN", "test-token")
    unauthorized = client.get("/api/v1/agents")
    assert unauthorized.status_code == 401
    assert unauthorized.json()["error"]["code"] == "http_401"

    authorized = client.get("/api/v1/agents", headers={"X-Local-Token": "test-token"})
    assert authorized.status_code == 200
    assert authorized.json()["success"] is True


def test_system_and_resource_routes_are_documented(client: TestClient) -> None:
    """The application exposes system endpoints and all Prompt 004 resource groups."""
    for path in ("/api/v1/system/health", "/api/v1/metrics", "/api/v1/version"):
        response = client.get(path)
        assert response.status_code == 200
        assert response.json()["success"] is True

    for path in (
        "/api/v1/agents",
        "/api/v1/videos",
        "/api/v1/workflows",
        "/api/v1/clips",
        "/api/v1/models",
        "/api/v1/settings",
    ):
        assert client.get(path).status_code == 200

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json()["paths"]
    assert "/api/v1/agents" in paths
    assert "/api/v1/videos" in paths
    assert "/api/v1/workflows/{workflow_id}/cancel" in paths
    assert "/api/v1/clips/{clip_id}/export" in paths
