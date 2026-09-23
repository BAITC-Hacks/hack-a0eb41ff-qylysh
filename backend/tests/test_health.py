from fastapi.testclient import TestClient

from app.api.router import api_router
from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "MoneyGraph API",
        "version": "0.1.0",
    }


def test_api_documentation_and_router_foundation() -> None:
    assert api_router.prefix == "/api/v1"
    assert client.get("/docs").status_code == 200

    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "MoneyGraph API"
    assert "/health" in response.json()["paths"]
    assert not any(path.startswith("/api/v1/") for path in response.json()["paths"])
