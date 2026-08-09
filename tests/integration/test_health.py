"""Foundation API integration tests."""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_health_endpoint() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["application"] == "ok"
    assert response.json()["data"]["database"] == "ok"


def test_system_info_endpoint() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/system/info")

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert response.json()["data"]["name"] == "ClipStudio AI"


def test_health_subroutes_and_request_id() -> None:
    with TestClient(create_app()) as client:
        response = client.get(
            "/health/system", headers={"X-Request-ID": "test-request"}
        )
        missing = client.get("/api/v1/does-not-exist")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "test-request"
    assert response.json()["success"] is True
    assert missing.status_code == 404
    assert missing.json()["success"] is False
