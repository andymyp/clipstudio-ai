"""Foundation API integration tests."""

from fastapi.testclient import TestClient

from backend.app.main import create_app


def test_health_endpoint() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["application"] == "ok"
    assert response.json()["database"] == "ok"


def test_system_info_endpoint() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/api/v1/system/info")

    assert response.status_code == 200
    assert response.json()["name"] == "ClipStudio AI"
