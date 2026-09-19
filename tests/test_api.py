from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_recommend():
    response = client.post(
        "/recommend",
        json={"user_id": "u1", "top_k": 5, "category": "technology"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["user_id"] == "u1"
    assert len(body["recommendations"]) == 5
