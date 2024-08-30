from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "working"}


def test_postgres_health_check():
    response = client.get("/healthcheck/postgres")
    assert response.status_code == 200
    assert response.json() == {"status_code": 200, "detail": "ok", "result": "postgres working"}
