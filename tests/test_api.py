from app.main import app


def test_health_endpoint():
    client = app.test_client()
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["status"] == "ok"


def test_invalid_provider_returns_400():
    client = app.test_client()
    res = client.get("/api/v1/earthquakes?provider=unknown")
    assert res.status_code == 400
    payload = res.get_json()
    assert "Unknown provider" in payload["error"]
